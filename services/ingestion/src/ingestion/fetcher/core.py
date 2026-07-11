import pathlib
import shutil
from typing import List
from structlog import get_logger
from .interface import DataFetcherProtocol

logger = get_logger(__name__)

class ManualDirectoryFetcher(DataFetcherProtocol):
    """Fetches files manually dropped into a watch directory."""
    def __init__(self, watch_dir: str, process_dir: str):
        self.watch_dir = pathlib.Path(watch_dir)
        self.process_dir = pathlib.Path(process_dir)
        self.watch_dir.mkdir(parents=True, exist_ok=True)
        self.process_dir.mkdir(parents=True, exist_ok=True)
        
    def fetch_recent(self) -> List[pathlib.Path]:
        """Moves files from watch_dir to process_dir and returns their new paths."""
        fetched_files = []
        for file_path in self.watch_dir.glob("*"):
            if file_path.is_file():
                dest_path = self.process_dir / file_path.name
                shutil.move(str(file_path), str(dest_path))
                fetched_files.append(dest_path)
                logger.info("fetched_file", source=str(file_path), dest=str(dest_path))
        return fetched_files

class ISSDCFetcher(DataFetcherProtocol):
    """Stub for automated PRADAN fetching from ISSDC."""
    def __init__(self, api_url: str, token: str, download_dir: str):
        self.api_url = api_url
        self.token = token
        self.download_dir = pathlib.Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)
        
    def fetch_recent(self) -> List[pathlib.Path]:
        """Fetches data from PRADAN."""
        logger.info("issdc_fetcher_stub_called", api=self.api_url)
        # TODO: Implement actual HTTP calls to PRADAN API.
        return []
