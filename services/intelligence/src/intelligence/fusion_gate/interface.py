from typing import Protocol, List
from shared.schemas.candidate import FlareCandidate

class FusionGateProtocol(Protocol):
    def fuse_candidates(self, solexs_candidates: List[FlareCandidate], hel1os_candidates: List[FlareCandidate]) -> List[FlareCandidate]:
        """Merges single-band candidates into confirmed or tentative master events."""
        ...
