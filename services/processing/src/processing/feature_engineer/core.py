import pandas as pd
import numpy as np
from structlog import get_logger
from .interface import FeatureEngineerProtocol

try:
    import pywt
except ImportError:
    pywt = None

logger = get_logger(__name__)

class LightCurveFeatureEngineer(FeatureEngineerProtocol):
    def compute_features(self, fused_data: pd.DataFrame) -> pd.DataFrame:
        logger.info("computing_features")
        df = fused_data.copy()
        
        # Use background subtracted fluxes if available, else fallback
        flux_cols = [col for col in df.columns if "flux_bg_subtracted" in col]
        if not flux_cols:
            flux_cols = [col for col in df.columns if "flux" in col and "high" not in col]
            
        for col in flux_cols:
            # Gradients
            df[f"{col}_grad"] = np.gradient(df[col])
            df[f"{col}_grad2"] = np.gradient(df[f"{col}_grad"])
            
            # Simplified wavelet feature (e.g. mean energy of details)
            if pywt is not None and len(df) >= 16:
                coeffs = pywt.wavedec(df[col], 'db2', level=2)
                df[f"{col}_wavelet_energy"] = np.mean(np.square(coeffs[0]))
            else:
                df[f"{col}_wavelet_energy"] = 0.0
                
        # Spectral Hardness
        low_col = next((c for c in df.columns if "bg_subtracted" in c and "high" not in c), None)
        high_col = next((c for c in df.columns if "bg_subtracted_high" in c), None)
        
        if low_col and high_col:
            df["spectral_hardness_ratio"] = df[high_col] / (df[low_col] + 1e-8)
            
        logger.info("feature_engineering_complete", features=len(df.columns))
        return df
