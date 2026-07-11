from typing import List
from structlog import get_logger
from datetime import timedelta
from .interface import FusionGateProtocol
from shared.schemas.candidate import FlareCandidate

logger = get_logger(__name__)

class DualBandConfidenceGate(FusionGateProtocol):
    def __init__(self, time_window_seconds: int = 60):
        self.time_window = timedelta(seconds=time_window_seconds)
        
    def fuse_candidates(self, solexs_candidates: List[FlareCandidate], hel1os_candidates: List[FlareCandidate]) -> List[FlareCandidate]:
        logger.info("fusing_candidates", solexs=len(solexs_candidates), hel1os=len(hel1os_candidates))
        
        fused_events = []
        matched_hel1os = set()
        
        for sc in solexs_candidates:
            match = next((hc for hc in hel1os_candidates if abs(hc.peak_time - sc.peak_time) <= self.time_window), None)
            
            if match:
                sc.confidence = 0.9 # CONFIRMED
                sc.band = "FUSED_DUAL_BAND"
                matched_hel1os.add(match.id)
            else:
                sc.confidence = 0.4 # TENTATIVE
                
            fused_events.append(sc)
            
        for hc in hel1os_candidates:
            if hc.id not in matched_hel1os:
                hc.confidence = 0.4 # TENTATIVE
                fused_events.append(hc)
                
        logger.info("fusion_gate_complete", total_fused=len(fused_events))
        return fused_events
