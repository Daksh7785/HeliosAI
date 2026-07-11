from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import timedelta
from shared.schemas.candidate import ForecastPrediction

class ReconciliationStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    EXPIRED = "EXPIRED"
    AWAITING = "AWAITING"

class ForecastReconciliationResult(BaseModel):
    status: ReconciliationStatus
    lead_time: Optional[timedelta]
    matched_catalogue_id: Optional[str]

class CatalogueQueryService:
    # Stub dependency
    pass

class LeadTimeReconciler:
    def reconcile(self, forecast: ForecastPrediction, catalogue: CatalogueQueryService) -> ForecastReconciliationResult:
        """Looks up whether a catalogue entry with peak_ts within
        [predicted_trigger_ts, predicted_trigger_ts + horizon_minutes] exists.
        If yes: lead_time = catalogue_entry.peak_ts - forecast.predicted_trigger_ts (Confirmed).
        If no, once horizon has elapsed: marks Expired (false positive)."""
        pass
