import pandas as pd
import numpy as np
from src.forecaster import create_features_and_labels

def test_create_features_and_labels():
    timestamps = pd.date_range("2024-01-01", periods=200, freq='s')
    df = pd.DataFrame({
        'timestamp': timestamps,
        'solexs_flux': np.random.rand(200),
        'helios_flux': np.random.rand(200)
    })
    
    flare_events = pd.DataFrame({
        'start_time': [pd.Timestamp("2024-01-01 00:02:00")],
        'end_time': [pd.Timestamp("2024-01-01 00:02:30")]
    })
    
    df_feat = create_features_and_labels(df, flare_events, lead_time_minutes=1, history_window=10)
    
    assert not df_feat.empty
    assert 'target_flare_in_N_min' in df_feat.columns
    assert 'solexs_flux_mean_10s' in df_feat.columns
    
    # Check if target logic works
    assert (df_feat['target_flare_in_N_min'] == 1).any()
