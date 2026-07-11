from typing import Protocol, Dict, Any

class PublisherProtocol(Protocol):
    def publish(self, valid_data: Dict[str, Any]) -> None:
        """Publishes validated data to the downstream processing queue."""
        ...
