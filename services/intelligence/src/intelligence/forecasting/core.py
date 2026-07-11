from typing import Any
from datetime import datetime
from structlog import get_logger
from .interface import ForecastingProtocol, LeadTimeEvaluatorProtocol

logger = get_logger(__name__)

class ClassicalBoostedForecaster(ForecastingProtocol):
    def __init__(self, model_path: str = None):
        self.model_path = model_path
        # In reality, this would load XGBoost/LightGBM model
        logger.info("initialized_classical_forecaster", path=model_path)
        
    def predict_probability(self, feature_sequence: Any, horizon_minutes: int) -> float:
        logger.debug("predicting_classical", horizon=horizon_minutes)
        # Mocking probability
        return 0.35

class DeepSequenceForecaster(ForecastingProtocol):
    def __init__(self, model_path: str = None, architecture: str = "TFT"):
        self.model_path = model_path
        self.architecture = architecture
        # In reality, this would load a PyTorch model (TFT, PatchTST, etc.)
        logger.info("initialized_deep_forecaster", architecture=architecture, path=model_path)
        
    def predict_probability(self, feature_sequence: Any, horizon_minutes: int) -> float:
        logger.debug("predicting_deep", architecture=self.architecture, horizon=horizon_minutes)
        # Mocking probability based on sequence input
        return 0.65

class LeadTimeTracker(LeadTimeEvaluatorProtocol):
    def calculate_empirical_lead_time(self, predicted_ts: datetime, actual_peak_ts: datetime) -> float:
        diff = (actual_peak_ts - predicted_ts).total_seconds()
        logger.info("calculated_lead_time", lead_time_seconds=diff)
        return diff
