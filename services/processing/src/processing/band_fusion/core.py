import pandas as pd
from structlog import get_logger
from .interface import FusionProtocol

logger = get_logger(__name__)

class CrossBandFuser(FusionProtocol):
    def fuse_bands(self, df_low: pd.DataFrame, df_high: pd.DataFrame) -> pd.DataFrame:
        logger.info("fusing_bands")
        
        if 'utc_time' not in df_low.columns or 'utc_time' not in df_high.columns:
            raise ValueError("DataFrames must have 'utc_time' column for fusion")
            
        df1 = df_low.copy().set_index('utc_time')
        df2 = df_high.copy().set_index('utc_time')
        
        # Rename overlapping columns to avoid confusion
        df2 = df2.add_suffix('_high')
        
        # Outer join on time index
        fused = df1.join(df2, how='outer')
        
        # Time-based interpolation
        fused = fused.interpolate(method='time')
        
        # Drop boundary NaNs
        fused = fused.dropna()
        
        logger.info("fusion_complete", rows=len(fused))
        return fused.reset_index()
