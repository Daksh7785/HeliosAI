from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class RawLightCurveRow(BaseModel):
    timestamp: datetime = Field(..., description="Observation timestamp in UTC")
    flux: float = Field(..., description="Measured flux value")
    energy_band: str = Field(..., description="Energy band (e.g., 'soft', 'hard')")
    instrument: str = Field(..., description="Instrument name ('solexs' or 'hel1os')")
    quality_flag: int = Field(default=0, description="0 = good, >0 = error/anomaly code")

class ProcessedLightCurveRow(BaseModel):
    timestamp: datetime = Field(..., description="Observation timestamp in UTC")
    flux: float = Field(..., description="Background-subtracted flux")
    flux_raw: float = Field(..., description="Original raw flux")
    background_level: float = Field(..., description="Estimated background level")
    energy_band: str = Field(..., description="Energy band")
    instrument: str = Field(..., description="Instrument name")

class FusedTelemetryRow(BaseModel):
    timestamp: datetime = Field(..., description="Synchronized observation timestamp in UTC")
    solexs_flux: float = Field(..., description="Soft X-ray flux from SoLEXS")
    hel1os_flux: float = Field(..., description="Hard X-ray counts from HEL1OS")
