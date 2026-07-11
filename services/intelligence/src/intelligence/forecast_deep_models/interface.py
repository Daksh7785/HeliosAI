from typing import Protocol, List
from shared.schemas.candidate import ForecastPrediction
from shared.schemas.lightcurve import EngineeredFeatureRow

class FeatureWindow:
    # Stub representation
    rows: List[EngineeredFeatureRow]

class FeatureWindowBuilder:
    def build_window(self, series: List[EngineeredFeatureRow], lookback_minutes: int) -> FeatureWindow:
        pass

class BaselineForecastModel(Protocol):
    def predict_proba(self, window: FeatureWindow, horizon_minutes: int) -> ForecastPrediction:
        pass

class XGBoostForecastModel(BaselineForecastModel):
    def __init__(self, model_run_id: str):
        pass

    def predict_proba(self, window: FeatureWindow, horizon_minutes: int) -> ForecastPrediction:
        pass

class DeepForecastModel(Protocol):
    def predict_proba(self, window: FeatureWindow, horizon_minutes: int) -> ForecastPrediction:
        pass

class PatchTSTForecastModel(DeepForecastModel):
    def __init__(self, model_run_id: str, checkpoint_uri: str):
        pass

    def predict_proba(self, window: FeatureWindow, horizon_minutes: int) -> ForecastPrediction:
        pass
