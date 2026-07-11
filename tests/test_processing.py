import pytest
import numpy as np
import pandas as pd

def test_preprocessing_median_filter():
    """
    Test the median filter logic from services/processing/src/processing/preprocess.py
    """
    from services.processing.src.processing.preprocess import Preprocessor
    processor = Preprocessor(filter_window=3)
    
    data = np.array([1.0, 100.0, 1.0, 1.0])
    filtered = processor.median_filter(data)
    
    assert filtered[1] == 1.0 # Spike removed
    
def test_time_synchronizer():
    """
    Test the time synchronization engine.
    """
    from services.processing.src.processing.sync import TimeSynchronizer
    sync = TimeSynchronizer(master_cadence_sec=1.0)
    
    start = pd.Timestamp("2026-07-03T00:00:00Z")
    end = pd.Timestamp("2026-07-03T00:00:02Z")
    
    solexs = pd.DataFrame({'flux': [1, 2]}, index=[start, end])
    hel1os = pd.DataFrame({'counts': [10, 20]}, index=[start, end])
    
    merged = sync.align_series(solexs, hel1os, start, end)
    assert len(merged) == 3 # 0s, 1s, 2s
    assert "solexs_flux" in merged.columns
    assert "hel1os_counts" in merged.columns
