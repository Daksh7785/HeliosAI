import pandas as pd
import numpy as np
from typing import List
from structlog import get_logger
from .interface import DetectorProtocol
from shared.schemas.candidate import FlareCandidate
from uuid import uuid4

logger = get_logger(__name__)

class GradientThresholdDetector(DetectorProtocol):
    def __init__(self, threshold_sigma: float = 3.0):
        self.threshold_sigma = threshold_sigma
        
    def detect_candidates(self, features_df: pd.DataFrame, band_prefix: str) -> List[FlareCandidate]:
        logger.info("detecting_candidates", band=band_prefix)
        candidates = []
        
        # Determine the correct column name based on fusion output
        # E.g. 'flux_bg_subtracted_grad' for low band, 'flux_bg_subtracted_high_grad' for high band
        suffix = "_high" if band_prefix.lower() == "hel1os" else ""
        grad_col = f"flux_bg_subtracted{suffix}_grad"
        flux_col = f"flux_bg_subtracted{suffix}"
        
        if grad_col not in features_df.columns:
            logger.warning("gradient_column_missing", expected_column=grad_col)
            return candidates
            
        mean_grad = features_df[grad_col].mean()
        std_grad = features_df[grad_col].std()
        threshold = mean_grad + (self.threshold_sigma * std_grad)
        
        exceeds = features_df[features_df[grad_col] > threshold]
        
        if not exceeds.empty:
            start_time = exceeds.iloc[0]['utc_time']
            end_time = exceeds.iloc[-1]['utc_time']
            peak_idx = exceeds[grad_col].idxmax()
            peak_time = exceeds.loc[peak_idx]['utc_time']
            peak_flux = exceeds.loc[peak_idx][flux_col] if flux_col in features_df.columns else 0.0
            
            candidate = FlareCandidate(
                id=str(uuid4()),
                band=band_prefix,
                start_time=start_time,
                end_time=end_time,
                peak_time=peak_time,
                peak_flux=peak_flux,
                confidence=0.5
            )
            candidates.append(candidate)
            
        logger.info("detection_complete", candidates_found=len(candidates), band=band_prefix)
        return candidates
