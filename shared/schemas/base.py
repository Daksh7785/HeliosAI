from pydantic import BaseModel, ConfigDict
from datetime import datetime

class HeliosBaseModel(BaseModel):
    """Base Pydantic model for all HeliosAI schemas."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class HeliosTimeStampedModel(HeliosBaseModel):
    """Base model with timestamps."""
    created_at: datetime
    updated_at: datetime
