from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import schema
from pydantic import BaseModel
from typing import List
import datetime

router = APIRouter()

class FlareCatalogueResponse(BaseModel):
    id: str
    start_time: datetime.datetime
    peak_time: datetime.datetime
    end_time: datetime.datetime
    goes_class_estimate: str | None
    peak_flux: float
    is_verified: bool

    class Config:
        from_attributes = True

@router.get("/catalogue", response_model=List[FlareCatalogueResponse])
def get_catalogue(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    catalogue = db.query(schema.FlareCatalogue).offset(skip).limit(limit).all()
    return catalogue

@router.get("/catalogue/{flare_id}", response_model=FlareCatalogueResponse)
def get_flare(flare_id: str, db: Session = Depends(get_db)):
    flare = db.query(schema.FlareCatalogue).filter(schema.FlareCatalogue.id == flare_id).first()
    if not flare:
        raise HTTPException(status_code=404, detail="Flare not found")
    return flare
