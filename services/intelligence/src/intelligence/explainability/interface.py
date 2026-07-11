from typing import Protocol, Any
from shared.schemas.candidate import FlareCandidate

class ExplainabilityProtocol(Protocol):
    def generate_explanation(self, event: FlareCandidate, model: Any, features: Any) -> dict:
        """Generates SHAP or similar explainability metrics for a detected/forecasted event."""
        ...
