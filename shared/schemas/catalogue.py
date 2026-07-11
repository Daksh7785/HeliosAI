from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FlareEventRow(BaseModel):
    event_id: str = Field(..., description="Unique event identifier (e.g., HELIOS-20261014-001)")
    start_time: datetime = Field(..., description="Flare start time")
    peak_time: datetime = Field(..., description="Flare peak time")
    end_time: Optional[datetime] = Field(None, description="Flare end time")
    goes_class: str = Field(..., description="Estimated GOES class (e.g., 'M2.3')")
    peak_flux_solexs: float = Field(..., description="Peak flux observed in SoLEXS")
    peak_flux_hel1os: Optional[float] = Field(None, description="Peak counts observed in HEL1OS")
    confidence: float = Field(..., description="Detection confidence score (0-1)")
    status: str = Field(..., description="'active', 'completed', or 'quarantined'")
