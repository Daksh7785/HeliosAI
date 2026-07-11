from typing import Protocol, List
from shared.schemas.candidate import FlareCandidate

class CatalogueProtocol(Protocol):
    def register_events(self, events: List[FlareCandidate]) -> None:
        """Registers fused events into the master catalogue database."""
        ...
