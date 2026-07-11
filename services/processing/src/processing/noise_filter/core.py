import pandas as pd
from structlog import get_logger
import scipy.signal as signal
from .interface import NoiseFilterProtocol

logger = get_logger(__name__)

class SavitzkyGolayFilter(NoiseFilterProtocol):
    def __init__(self, window_length: int = 11, polyorder: int = 3):
        self.window_length = window_length
        self.polyorder = polyorder
        
    def filter_noise(self, data: pd.DataFrame, flux_column: str = "flux") -> pd.DataFrame:
        logger.info("filtering_noise", flux_column=flux_column)
        df = data.copy()
        
        if flux_column not in df.columns:
            raise ValueError(f"Column {flux_column} not found in dataframe.")
            
        # Handle NaNs via interpolation before filtering
        flux_data = df[flux_column].interpolate(method='linear', limit_direction='both')
        
        if len(flux_data) >= self.window_length:
            smoothed = signal.savgol_filter(flux_data, self.window_length, self.polyorder)
            df[f"{flux_column}_smoothed"] = smoothed
        else:
            df[f"{flux_column}_smoothed"] = flux_data
            
        # Simple background subtraction
        background = flux_data.rolling(window=50, min_periods=1, center=True).min().interpolate(method='linear', limit_direction='both')
        df[f"{flux_column}_bg_subtracted"] = df[f"{flux_column}_smoothed"] - background
        
        logger.info("noise_filtering_complete", rows=len(df))
        return df
