from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import List, Optional
from shared.schemas.lightcurve import Instrument

class FlareClass(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    M = "M"
    X = "X"

class FusedFlareCandidate(BaseModel):
    start_ts: datetime
    peak_ts: datetime
    end_ts: datetime
    peak_flux_solexs: Optional[float]
    peak_flux_hel1os: Optional[float]
    confidence: float               # 0.0 - 1.0
    bands_agreeing: List[Instrument]
    tentative: bool

class ClassifiedFlareCandidate(FusedFlareCandidate):
    flare_class: FlareClass
    model_run_id: str
    data_snapshot_id: str
    explanation_ref: Optional[str]

class ForecastPrediction(BaseModel):
    horizon_minutes: int
    probability: float              # 0.0 - 1.0
    predicted_class_if_occurs: Optional[FlareClass]
    predicted_trigger_ts: datetime
    model_run_id: str
    data_snapshot_id: str
    explanation_ref: Optional[str]

class ExplanationArtifactRef(BaseModel):
    artifact_id: str
    method: str                     # "shap" | "integrated_gradients" | "attention"
    storage_uri: str
