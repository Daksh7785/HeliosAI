from typing import Protocol
import pandas as pd

class FeatureEngineerProtocol(Protocol):
    def compute_features(self, fused_data: pd.DataFrame) -> pd.DataFrame:
        """Computes derived features on fused time-series data."""
        ...
