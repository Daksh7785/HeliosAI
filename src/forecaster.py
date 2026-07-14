import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os
import sys

# Ensure intelligence module can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../services/intelligence/src/intelligence')))
from forecast_deep_models.lstm_model import train_pytorch_lstm, predict_pytorch_lstm

def create_features_and_labels(df, flare_events, lead_time_minutes=30, history_window=60):
    """
    Creates feature set and labels for forecasting.
    Target: 1 if a flare starts within the next `lead_time_minutes`, else 0.
    Features: Rolling statistics of soft and hard X-rays over `history_window` seconds.
    """
    df = df.copy()
    
    # Feature Engineering
    for col in ['solexs_flux', 'helios_flux']:
        df[f'{col}_mean_{history_window}s'] = df[col].rolling(window=history_window).mean()
        df[f'{col}_std_{history_window}s'] = df[col].rolling(window=history_window).std()
        df[f'{col}_max_{history_window}s'] = df[col].rolling(window=history_window).max()
        # Derivative (rate of change) over window
        df[f'{col}_diff_{history_window}s'] = df[col].diff(periods=history_window)
    
    # Drop NaNs introduced by rolling windows
    df = df.dropna().reset_index(drop=True)
    
    # Create target label
    # A positive sample is any time step that is within `lead_time_minutes` BEFORE a flare start.
    df['target_flare_in_N_min'] = 0
    
    for _, event in flare_events.iterrows():
        start_time = event['start_time']
        # Define the pre-flare window (lead time)
        pre_flare_start = start_time - pd.Timedelta(minutes=lead_time_minutes)
        
        # Mark target as 1 in this window
        mask = (df['timestamp'] >= pre_flare_start) & (df['timestamp'] < start_time)
        df.loc[mask, 'target_flare_in_N_min'] = 1
        
    # We will exclude the actual flare times from the training set to focus strictly on pre-flare precursors
    for _, event in flare_events.iterrows():
        mask = (df['timestamp'] >= event['start_time']) & (df['timestamp'] <= event['end_time'])
        df = df[~mask]
        
    return df.reset_index(drop=True)

def train_forecasting_model(df_features, lead_time_minutes=15, model_path='models/xgboost_forecaster.pkl'):
    """
    Trains an XGBoost model to forecast flares.
    Calculates TPR, FAR, and Lead Time metrics.
    """
    features = [c for c in df_features.columns if c not in ['timestamp', 'target_flare_in_N_min', 'solexs_flux', 'helios_flux', 'soft_baseline', 'soft_mad', 'soft_flare_detected', 'hard_baseline', 'hard_mad', 'hard_flare_detected', 'flare_active', 'flare_class', 'event_group', 'data_quality_flag']]
    
    X = df_features[features]
    y = df_features['target_flare_in_N_min']
    
    # Simple temporal split (first 80% train, last 20% test)
    split_idx = int(len(df_features) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    # Train XGBoost
    # Using scale_pos_weight since classes are highly imbalanced (flares are rare)
    scale_weight = len(y_train[y_train==0]) / max(1, len(y_train[y_train==1]))
    model = XGBClassifier(
        n_estimators=100, 
        learning_rate=0.1, 
        max_depth=5, 
        scale_pos_weight=scale_weight,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    print("--- Forecasting Model Evaluation ---")
    print(classification_report(y_test, preds))
    
    # Calculate Custom Metrics
    cm = confusion_matrix(y_test, preds)
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        far = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    else:
        tpr = 0.0
        far = 0.0
        
    metrics = {
        'TPR': tpr,
        'FAR': far,
        'Lead_Time_Minutes': lead_time_minutes
    }
    print(f"TPR: {tpr:.2f}, FAR: {far:.2f}, Lead Time: {lead_time_minutes} min")
    
    # Save model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    joblib.dump(features, model_path.replace('.pkl', '_features.pkl'))
    joblib.dump(metrics, model_path.replace('.pkl', '_metrics.pkl'))
    print(f"Model saved to {model_path}")
    
    return model, metrics

def train_lstm_forecasting_model(df_features, lead_time_minutes=15, model_path='models/lstm_forecaster.pkl', seq_length=10):
    """
    Trains a PyTorch LSTM model to forecast flares.
    Calculates TPR, FAR, and Lead Time metrics.
    """
    features = [c for c in df_features.columns if c not in ['timestamp', 'target_flare_in_N_min', 'solexs_flux', 'helios_flux', 'soft_baseline', 'soft_mad', 'soft_flare_detected', 'hard_baseline', 'hard_mad', 'hard_flare_detected', 'flare_active', 'flare_class', 'event_group', 'data_quality_flag']]
    
    X = df_features[features]
    y = df_features['target_flare_in_N_min']
    
    # Simple temporal split (first 80% train, last 20% test)
    split_idx = int(len(df_features) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    # Train LSTM
    model = train_pytorch_lstm(X_train, y_train, input_dim=len(features), epochs=5, batch_size=64, seq_length=seq_length)
    
    # Evaluate
    preds_prob = predict_pytorch_lstm(model, X_test, seq_length=seq_length)
    preds = (preds_prob > 0.5).astype(int)
    
    print("--- LSTM Forecasting Model Evaluation ---")
    print(classification_report(y_test, preds))
    
    # Calculate Custom Metrics
    cm = confusion_matrix(y_test, preds)
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        far = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    else:
        tpr = 0.0
        far = 0.0
        
    metrics = {
        'TPR': tpr,
        'FAR': far,
        'Lead_Time_Minutes': lead_time_minutes
    }
    print(f"TPR: {tpr:.2f}, FAR: {far:.2f}, Lead Time: {lead_time_minutes} min")
    
    # Save model and features using torch/joblib
    import torch
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    torch.save(model.state_dict(), model_path)
    joblib.dump(features, model_path.replace('.pkl', '_features.pkl'))
    joblib.dump(metrics, model_path.replace('.pkl', '_metrics.pkl'))
    print(f"Model saved to {model_path}")
    
    return model, metrics

if __name__ == "__main__":
    from data_loader import load_and_merge_data
    from flare_detector import detect_flares
    
    print("Loading data...")
    df = load_and_merge_data('data/solexs_simulated.csv', 'data/helios_simulated.csv')
    print("Detecting flares to get ground truth...")
    df_processed, flare_events = detect_flares(df)
    
    print("Creating features for forecasting...")
    df_features = create_features_and_labels(df_processed, flare_events, lead_time_minutes=15)
    
    print("Training model...")
    train_forecasting_model(df_features)
    train_lstm_forecasting_model(df_features)
