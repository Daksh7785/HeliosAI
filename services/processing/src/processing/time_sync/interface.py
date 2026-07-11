from typing import Protocol
import pandas as pd

class TimeSyncProtocol(Protocol):
    def sync_time(self, data: pd.DataFrame, instrument: str) -> pd.DataFrame:
        """Synchronizes instrument-specific time to UTC."""
        ...
