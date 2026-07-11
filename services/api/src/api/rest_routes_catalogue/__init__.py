from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from shared.db.session import get_db
from shared.schemas.catalogue import FlareEventRow

router = APIRouter()

@router.get("/", response_model=List[FlareEventRow])
def list_catalogue(
    db: Session = Depends(get_db),
    limit: int = 100
):
    """
    Fetch historical flare events.
    """
    # Placeholder returning empty list
    return []
