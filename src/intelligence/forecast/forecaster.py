import pandas as pd
import xgboost as xgb
from src.intelligence.base_model import BaseModelPredictor

class XGBoostForecaster(BaseModelPredictor):
    """
    Forecasting engine to predict flare probability in the next 30 minutes.
    """
    def __init__(self, model_path=None):
        self.model = xgb.XGBClassifier()
        if model_path:
            self.load_model(model_path)
        else:
            self.is_trained = False
            
    def load_model(self, path: str):
        self.model.load_model(path)
        self.is_trained = True
        
    def save_model(self, path: str):
        self.model.save_model(path)

    def train(self, X: pd.DataFrame, y: pd.Series):
        """
        Train the forecasting model.
        """
        self.model.fit(X, y)
        self.is_trained = True

    def predict(self, feature_df: pd.DataFrame) -> pd.DataFrame:
        """
        Takes recent feature timeseries and predicts if a flare will happen soon.
        Returns the probability.
        """
        if not self.is_trained:
            # Mock untrained behavior
            return pd.DataFrame()
            
        # Extract features
        X = feature_df[['solexs_flux', 'hel1os_flux', 'hardness_ratio']]
        
        # Predict probability
        probs = self.model.predict_proba(X)[:, 1]
        
        results = feature_df.copy()
        results['flare_probability'] = probs
        return results
