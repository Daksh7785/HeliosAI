from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict

class ForecastResponse(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time the forecast was generated")
    target_window_minutes: int = Field(..., description="Forecast window (e.g., 60 for 1-hour)")
    prob_c_class: float = Field(..., description="Probability of C-class flare (0-1)")
    prob_m_class: float = Field(..., description="Probability of M-class flare (0-1)")
    prob_x_class: float = Field(..., description="Probability of X-class flare (0-1)")
    model_version: str = Field(..., description="The MLflow model version used for inference")
    feature_contributions: Dict[str, float] = Field(default_factory=dict, description="SHAP/importance values")
