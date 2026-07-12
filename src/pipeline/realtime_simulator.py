import sys
import os
import time
import asyncio
import pandas as pd
import joblib
from sqlalchemy.ext.asyncio import AsyncSession
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.data_loader import load_and_merge_data, generate_simulated_data
from src.flare_detector import detect_flares
from src.forecaster import create_features_and_labels, train_forecasting_model
from src.shared.database.db import get_db, engine
from src.shared.database.models import Base, FeatureStore, FlareCatalogue

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def simulate_realtime(df, model, features_cols):
    # Simulate streaming
    # We will step through the dataframe 
    # For a realistic simulation, we would use a rolling window of past N points
    
    # Let's clear the FeatureStore first for a clean simulation
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    window_size = 60 # Needs at least history_window
    
    async for db in get_db():
        for i in range(window_size, len(df), 10): # step by 10 for speed
            window = df.iloc[i-window_size:i].copy()
            
            # Nowcast
            df_nowcast, _ = detect_flares(window)
            latest_nowcast = df_nowcast.iloc[-1]
            
            # Forecast
            # We need to construct features exactly as the model expects
            for col in ['solexs_flux', 'helios_flux']:
                window[f'{col}_mean_{window_size}s'] = window[col].rolling(window=window_size).mean()
                window[f'{col}_std_{window_size}s'] = window[col].rolling(window=window_size).std()
                window[f'{col}_max_{window_size}s'] = window[col].rolling(window=window_size).max()
                window[f'{col}_diff_{window_size}s'] = window[col].diff(periods=window_size-1) # Approximate diff
                
            latest_features = window.iloc[[-1]].fillna(0)
            X = latest_features[features_cols]
            
            prob = float(model.predict_proba(X)[0][1])
            
            import json
            # XAI: Get top features based on global feature importance scaled by actual values
            # This is a simplified XAI approximation for real-time speed.
            importance = model.feature_importances_
            feature_contributions = importance * X.iloc[0].values
            top_idx = feature_contributions.argsort()[-3:][::-1]
            top_features_list = [features_cols[i] for i in top_idx]
            xai_json = json.dumps(top_features_list)
            
            quality_flag = str(latest_nowcast.get('data_quality_flag', 'VALIDATED'))
            
            # Save to DB
            new_feature = FeatureStore(
                timestamp=latest_nowcast['timestamp'].to_pydatetime(),
                solexs_flux=float(latest_nowcast['solexs_flux']),
                hel1os_flux=float(latest_nowcast['helios_flux']),
                hardness_ratio=float(latest_nowcast['helios_flux'] / max(1e-10, latest_nowcast['solexs_flux'])),
                is_flare_candidate=bool(latest_nowcast.get('flare_active', False)),
                forecast_probability=prob,
                xai_top_features=xai_json,
                data_quality_flag=quality_flag
            )
            
            db.add(new_feature)
            await db.commit()
            
            print(f"[{latest_nowcast['timestamp']}] SoLEXS: {latest_nowcast['solexs_flux']:.2e}, HEL1OS: {latest_nowcast['helios_flux']:.2e} | Flare: {new_feature.is_flare_candidate} | Forecast Prob: {prob:.2f}")
            time.sleep(1) # Simulate real-time delay (1s per batch of 10s)

async def main():
    await init_db()
    
    solexs_path = 'data/solexs_simulated.csv'
    helios_path = 'data/helios_simulated.csv'
    model_path = 'models/xgboost_forecaster.pkl'
    
    if not os.path.exists(solexs_path):
        print("Generating data...")
        generate_simulated_data()
        
    df = load_and_merge_data(solexs_path, helios_path)
    
    if not os.path.exists(model_path):
        print("Training model...")
        df_processed, flare_events = detect_flares(df)
        df_features = create_features_and_labels(df_processed, flare_events, lead_time_minutes=15)
        model = train_forecasting_model(df_features, model_path)
    else:
        model = joblib.load(model_path)
        
    features_cols = joblib.load(model_path.replace('.pkl', '_features.pkl'))
    
    print("Starting real-time simulation...")
    await simulate_realtime(df, model, features_cols)

if __name__ == "__main__":
    asyncio.run(main())
