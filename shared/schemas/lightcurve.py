from pydantic import BaseModel, field_validator
from datetime import datetime
from enum import Enum
from typing import List

class Instrument(str, Enum):
    SOLEXS = "solexs"
    HEL1OS = "hel1os"

class RawLightCurvePoint(BaseModel):
    instrument: Instrument
    spacecraft_time: float          # raw onboard clock value
    flux: float
    energy_channel: str
    quality_flag: int

    @field_validator("flux")
    @classmethod
    def flux_non_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError("flux must be non-negative")
        return v

class RawLightCurveBatch(BaseModel):
    instrument: Instrument
    source_file: str
    ingested_at: datetime
    points: List[RawLightCurvePoint]
    correlation_id: str

class ProcessedLightCurvePoint(BaseModel):
    instrument: Instrument
    utc_timestamp: datetime
    flux_cleaned: float
    background_level: float
    data_quality_flags: List[str]

class EngineeredFeatureRow(BaseModel):
    utc_timestamp: datetime
    solexs_flux: float
    hel1os_flux: float
    hardness_ratio: float
    flux_gradient_solexs: float
    flux_gradient_hel1os: float
    wavelet_energy_solexs: float
    wavelet_energy_hel1os: float
    data_snapshot_id: str
