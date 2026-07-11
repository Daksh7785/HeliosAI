from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from shared.db.session import get_db
from shared.schemas.lightcurve import FusedTelemetryRow

router = APIRouter()

@router.get("/live", response_model=List[FusedTelemetryRow])
def get_live_lightcurve(
    db: Session = Depends(get_db),
    minutes: int = 60
):
    """
    Fetch the most recent light curve data.
    """
    # Placeholder: In a real scenario, this queries TimescaleDB
    return [
        FusedTelemetryRow(
            timestamp=datetime.utcnow(),
            solexs_flux=1.2e-7,
            hel1os_flux=0.0
        )
    ]
