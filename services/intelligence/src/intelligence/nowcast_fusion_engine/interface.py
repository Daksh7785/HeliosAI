from typing import List
from shared.schemas.candidate import FusedFlareCandidate
from services.intelligence.nowcast_detector import BandFlareCandidate

class FusionEngine:
    def fuse(self, solexs_candidates: List[BandFlareCandidate],
             hel1os_candidates: List[BandFlareCandidate]) -> List[FusedFlareCandidate]:
        """Time-window overlap matching between band candidates; computes
        a confidence score; marks unmatched single-band candidates tentative."""
        pass
