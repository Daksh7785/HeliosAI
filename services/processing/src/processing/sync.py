import numpy as np
import pandas as pd
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class TimeSynchronizer:
    """
    Time Synchronization Engine (Doc 19)
    Aligns asynchronous telemetry streams from SoLEXS and HEL1OS to a master cadence.
    """
    def __init__(self, master_cadence_sec: float = 1.0):
        self.master_cadence_sec = master_cadence_sec

    def align_series(self, 
                     solexs_data: pd.DataFrame, 
                     hel1os_data: pd.DataFrame, 
                     start_time: pd.Timestamp, 
                     end_time: pd.Timestamp) -> pd.DataFrame:
        """
        Interpolates and aligns both instruments onto a unified timeline.
        Assumes dataframes have a datetime index.
        """
        logger.info(f"Synchronizing streams to {self.master_cadence_sec}s cadence.")
        
        # Create master time index
        master_index = pd.date_range(start=start_time, end=end_time, freq=f"{self.master_cadence_sec}S")
        
        # Reindex and interpolate SoLEXS
        solexs_aligned = solexs_data.reindex(master_index.union(solexs_data.index))
        solexs_aligned = solexs_aligned.interpolate(method='time').reindex(master_index)
        
        # Reindex and interpolate HEL1OS
        hel1os_aligned = hel1os_data.reindex(master_index.union(hel1os_data.index))
        hel1os_aligned = hel1os_aligned.interpolate(method='time').reindex(master_index)
        
        # Merge into synchronized dataframe
        merged = pd.concat([solexs_aligned, hel1os_aligned], axis=1)
        merged.columns = [f"solexs_{c}" for c in solexs_aligned.columns] + \
                         [f"hel1os_{c}" for c in hel1os_aligned.columns]
                         
        return merged
