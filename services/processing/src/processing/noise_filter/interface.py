from typing import Protocol
import pandas as pd

class NoiseFilterProtocol(Protocol):
    def filter_noise(self, data: pd.DataFrame, flux_column: str = "flux") -> pd.DataFrame:
        """Applies noise filtering and background subtraction."""
        ...
