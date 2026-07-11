from typing import Protocol
import pandas as pd

class FusionProtocol(Protocol):
    def fuse_bands(self, df_low: pd.DataFrame, df_high: pd.DataFrame) -> pd.DataFrame:
        """Merges two instrument dataframes into a single time-aligned dataframe."""
        ...
