from abc import ABC, abstractmethod
import pandas as pd

class BaseModelPredictor(ABC):
    """
    Interface for all Intelligence modules (Nowcast and Forecast).
    """
    
    @abstractmethod
    def predict(self, feature_df: pd.DataFrame) -> pd.DataFrame:
        """
        Takes a synchronized feature DataFrame (from FeatureStore) 
        and returns a DataFrame with predictions (e.g. is_flare, probability).
        """
        pass
    
    @abstractmethod
    def load_model(self, path: str):
        """
        Loads the underlying model weights/config.
        """
        pass

    @abstractmethod
    def save_model(self, path: str):
        """
        Saves the underlying model weights/config.
        """
        pass
