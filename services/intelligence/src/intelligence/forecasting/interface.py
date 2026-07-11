from typing import Protocol, Any
from datetime import datetime

class ForecastingProtocol(Protocol):
    def predict_probability(self, feature_sequence: Any, horizon_minutes: int) -> float:
        """Predicts the probability of a flare occurring within the horizon_minutes."""
        ...

class LeadTimeEvaluatorProtocol(Protocol):
    def calculate_empirical_lead_time(self, predicted_ts: datetime, actual_peak_ts: datetime) -> float:
        """Computes empirical lead time in seconds between prediction and actual peak."""
        ...
