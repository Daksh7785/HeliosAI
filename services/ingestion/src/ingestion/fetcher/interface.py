from typing import Protocol, List
import pathlib

class DataFetcherProtocol(Protocol):
    def fetch_recent(self) -> List[pathlib.Path]:
        """Fetches recent data files and returns a list of local paths to them."""
        ...
