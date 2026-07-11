from typing import Protocol, Dict, Any

class DataValidatorProtocol(Protocol):
    def validate(self, parsed_data: Dict[str, Any]) -> bool:
        """Validates parsed data and raises IngestionError on failure, or returns True."""
        ...
