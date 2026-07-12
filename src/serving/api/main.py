from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List
from datetime import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.shared.database.db import get_db
from src.shared.database.models import FeatureStore, FlareCatalogue

app = FastAPI(title="HeliosAI API", description="Space Weather Intelligence Platform")

class FeatureResponse(BaseModel):
    timestamp: datetime
    solexs_flux: float
    hel1os_flux: float
    hardness_ratio: float
    is_flare_candidate: bool
    forecast_probability: float | None = None
    xai_top_features: str | None = None
    data_quality_flag: str = "RAW"

    class Config:
        from_attributes = True

class CatalogueResponse(BaseModel):
    start_time: datetime
    peak_time: datetime
    end_time: datetime | None
    class_level: str | None
    peak_flux: float
    source: str

    class Config:
        from_attributes = True

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}

@app.get("/api/v1/telemetry/recent", response_model=List[FeatureResponse])
async def get_recent_telemetry(limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Fetch the most recent processed features for plotting."""
    result = await db.execute(select(FeatureStore).order_by(FeatureStore.timestamp.desc()).limit(limit))
    records = result.scalars().all()
    # Reverse to return chronological order for plotting
    return records[::-1]

@app.get("/api/v1/catalogue/recent", response_model=List[CatalogueResponse])
async def get_recent_flares(limit: int = 10, db: AsyncSession = Depends(get_db)):
    """Fetch the recent detected flares."""
    result = await db.execute(select(FlareCatalogue).order_by(FlareCatalogue.start_time.desc()).limit(limit))
    records = result.scalars().all()
    return records
