import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, Optional
from datetime import datetime

class Nowcaster:
    """
    Implements the Nowcasting algorithm:
    1. Per-Band Detection (Threshold + Changepoint)
    2. Event Characterization
    3. Cross-Band Confidence Fusion
    4. Master Catalogue Promotion Rules
    """
    def __init__(self, solexs_threshold: float = 1e-6, hel1os_threshold: float = 1e-6):
        self.solexs_threshold = solexs_threshold
        self.hel1os_threshold = hel1os_threshold

    def _threshold_detector(self, flux: pd.Series, threshold: float) -> bool:
        """Flags a candidate if background-subtracted flux crosses a threshold."""
        return bool(np.any(flux > threshold))

    def _changepoint_detector(self, flux: pd.Series) -> bool:
        """
        Flags a statistically significant shift in local mean/slope.
        For real-time, this would use a DWT-based or fast rolling metric.
        Here we use a simple rolling difference as a proxy for the changepoint.
        """
        if len(flux) < 5:
            return False
        rolling_mean = flux.rolling(window=3).mean()
        diff = rolling_mean.diff()
        # Simplified changepoint logic: sudden large positive slope
        return bool(np.any(diff > (flux.std() * 3)))

    def detect_band(self, flux: pd.Series, threshold: float) -> bool:
        """Runs both detectors in parallel for a band. Candidate raised if either fires."""
        return self._threshold_detector(flux, threshold) or self._changepoint_detector(flux)

    def _characterize_event(self, flux: pd.Series, times: pd.Series) -> Dict[str, Any]:
        """Calculates peak time/magnitude, rise time, decay time."""
        if len(flux) == 0:
            return {}
            
        peak_idx = flux.idxmax()
        peak_mag = flux.loc[peak_idx]
        peak_time = times.loc[peak_idx]
        
        # Simplified rise/decay time approximations
        onset_idx = flux.index[0]
        rise_time = (peak_time - times.loc[onset_idx]).total_seconds()
        
        # Decay time (e-folding) approximated
        decay_time = rise_time * 2.0 
        
        return {
            "peak_time": peak_time,
            "peak_magnitude": peak_mag,
            "rise_time_sec": rise_time,
            "decay_time_sec": decay_time
        }

    def _assign_goes_class(self, peak_flux: float) -> str:
        """Assigns GOES-equivalent class based on SoLEXS peak flux."""
        if peak_flux >= 1e-4:
            return "X"
        elif peak_flux >= 1e-5:
            return "M"
        elif peak_flux >= 1e-6:
            return "C"
        elif peak_flux >= 1e-7:
            return "B"
        return "A"

    def run_nowcast(self, features_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Consumes fused features, runs detection, fusion, and promotion rules.
        Expected columns: 'timestamp', 'solexs_flux', 'hel1os_flux', 'hardness_ratio', 'cross_band_agreement_flag'
        """
        if features_df.empty:
            return {"status": "No event"}

        times = features_df["timestamp"]
        solexs_flux = features_df["solexs_flux"]
        hel1os_flux = features_df["hel1os_flux"]

        # 1. Per-Band Detection
        solexs_detected = self.detect_band(solexs_flux, self.solexs_threshold)
        hel1os_detected = self.detect_band(hel1os_flux, self.hel1os_threshold)

        if not solexs_detected and not hel1os_detected:
            return {"status": "No event"}

        # 2. Event Characterization
        solexs_char = self._characterize_event(solexs_flux, times) if solexs_detected else {}
        hel1os_char = self._characterize_event(hel1os_flux, times) if hel1os_detected else {}
        
        goes_class = self._assign_goes_class(solexs_char.get("peak_magnitude", 0.0)) if solexs_detected else "Unknown"

        # 3. Cross-Band Confidence Fusion
        # Assuming cross_band_agreement_flag is pre-calculated in features, or we compute it here.
        # We will compute it here as a simple boolean AND for the tolerance window.
        both_agree = solexs_detected and hel1os_detected
        
        if both_agree:
            confidence = "High"
            status = "Promoted"
            confidence_score = 0.95
        elif solexs_detected:
            confidence = "Medium"
            status = "Tentative"
            confidence_score = 0.60
        else: # hel1os only
            confidence = "Medium-low"
            status = "Tentative"
            confidence_score = 0.30

        # 4. Master Catalogue Promotion Rules
        # Return structured event record
        return {
            "status": status,
            "confidence": confidence,
            "confidence_score": confidence_score,
            "class": goes_class,
            "peak_time": solexs_char.get("peak_time") or hel1os_char.get("peak_time"),
            "solexs_peak": solexs_char.get("peak_magnitude"),
            "hel1os_peak": hel1os_char.get("peak_magnitude"),
            "model_version": "nowcast_v0.1",
            "timestamp_processed": datetime.utcnow()
        }
