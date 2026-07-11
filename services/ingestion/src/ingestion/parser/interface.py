from typing import Protocol, Dict, Any
import pathlib

class FormatParserProtocol(Protocol):
    def parse(self, file_path: pathlib.Path) -> Dict[str, Any]:
        """Parses a raw data file and returns a structured dictionary representation."""
        ...
