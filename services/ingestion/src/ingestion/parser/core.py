import pathlib
from typing import Dict, Any
from structlog import get_logger
from .interface import FormatParserProtocol

logger = get_logger(__name__)

class FITSParser(FormatParserProtocol):
    """Parses FITS format files (expected from PRADAN L1 data)."""
    def parse(self, file_path: pathlib.Path) -> Dict[str, Any]:
        # Using astropy locally inside the function to avoid importing if not installed yet
        from astropy.io import fits
        
        logger.info("parsing_fits_file", file=str(file_path))
        data = {"file_name": file_path.name, "format": "FITS", "header": {}, "data": []}
        try:
            with fits.open(file_path) as hdul:
                # Stub implementation: grab header from primary HDU and data from first extension
                primary_header = hdul[0].header
                data["header"] = dict(primary_header)
                if len(hdul) > 1:
                    table_data = hdul[1].data
                    # Convert to a list of dicts or standard structures if needed
                    # Note: this is a stub for real extraction
                    data["data_length"] = len(table_data)
        except Exception as e:
            logger.error("fits_parsing_failed", error=str(e), file=str(file_path))
            raise
        return data

class CSVParser(FormatParserProtocol):
    """Parses standard CSV light curve files (fallback)."""
    def parse(self, file_path: pathlib.Path) -> Dict[str, Any]:
        import pandas as pd
        
        logger.info("parsing_csv_file", file=str(file_path))
        try:
            df = pd.read_csv(file_path)
            return {
                "file_name": file_path.name,
                "format": "CSV",
                "columns": list(df.columns),
                "data_length": len(df)
            }
        except Exception as e:
            logger.error("csv_parsing_failed", error=str(e), file=str(file_path))
            raise
