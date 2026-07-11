import sys
import os
from typing import Dict, Any
from structlog import get_logger

# Fix path for heliosai_shared import if running locally
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../")))
try:
    from shared.exceptions.errors import IngestionError
except ImportError:
    class IngestionError(Exception):
        pass

from .interface import DataValidatorProtocol

logger = get_logger(__name__)

class LightCurveValidator(DataValidatorProtocol):
    """Validates raw parsed light curve data structure."""
    
    def validate(self, parsed_data: Dict[str, Any]) -> bool:
        """
        Validates that required fields exist and basic constraints hold.
        Raises IngestionError if validation fails.
        """
        logger.info("validating_data", file_name=parsed_data.get("file_name"))
        
        if "data_length" not in parsed_data:
            raise IngestionError("Missing 'data_length' in parsed data.")
            
        if parsed_data["data_length"] == 0:
            raise IngestionError("Parsed data is empty.")
            
        if parsed_data.get("format") not in ["FITS", "CSV"]:
            raise IngestionError(f"Unsupported format: {parsed_data.get('format')}")
            
        # Additional checks for gap thresholds or negative timestamps could be added here
        logger.info("validation_successful", file_name=parsed_data.get("file_name"))
        return True
