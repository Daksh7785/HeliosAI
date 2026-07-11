from typing import Protocol
import pandas as pd

class PersistenceWriterProtocol(Protocol):
    def write_features(self, features_df: pd.DataFrame, table_name: str = "engineered_features") -> None:
        """Writes the engineered features dataframe to the database."""
        ...
