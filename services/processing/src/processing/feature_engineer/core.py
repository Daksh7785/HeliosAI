import pandas as pd
import numpy as np

def calculate_rolling_variance(df: pd.DataFrame, window: str = "5T") -> pd.DataFrame:
    """
    Calculates the rolling variance over the specified time window.
    Assumes df has a DateTimeIndex.
    """
    if "flux" not in df.columns:
        raise ValueError("DataFrame must contain a 'flux' column.")
    
    df["rolling_variance"] = df["flux"].rolling(window=window).var()
    return df

def calculate_spectral_hardness(solexs_flux: pd.Series, hel1os_counts: pd.Series) -> pd.Series:
    """
    Calculates the hardness ratio between Hard X-rays and Soft X-rays.
    Ratio = HEL1OS / SoLEXS
    """
    return hel1os_counts / (solexs_flux + 1e-12) # Add epsilon to avoid div by zero
