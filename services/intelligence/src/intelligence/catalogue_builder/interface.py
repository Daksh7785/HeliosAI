from shared.schemas.candidate import ClassifiedFlareCandidate, ForecastPrediction
from pydantic import BaseModel

class FlareCatalogueRow(BaseModel):
    # Stub representation
    pass

class ForecastEventRow(BaseModel):
    # Stub representation
    pass

class CatalogueBuilder:
    def build_catalogue_entry(self, classified: ClassifiedFlareCandidate) -> FlareCatalogueRow:
        pass

    def build_forecast_entry(self, prediction: ForecastPrediction) -> ForecastEventRow:
        pass
