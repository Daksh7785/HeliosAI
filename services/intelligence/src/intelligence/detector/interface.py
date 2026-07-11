from typing import Protocol, List
import pandas as pd
from shared.schemas.candidate import FlareCandidate

class DetectorProtocol(Protocol):
    def detect_candidates(self, features_df: pd.DataFrame, band_prefix: str) -> List[FlareCandidate]:
        """Detects single-band flare candidates from the feature dataframe."""
        ...
