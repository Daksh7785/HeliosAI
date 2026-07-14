import pandas as pd
import numpy as np
from src.flare_detector import detect_flares

def test_detect_flares_no_data():
    df = pd.DataFrame(columns=['timestamp', 'solexs_flux', 'helios_flux'])
    df_out, cat = detect_flares(df)
    assert df_out.empty
    assert cat.empty

def test_detect_flares_with_synthetic_spike():
    timestamps = pd.date_range("2024-01-01", periods=100, freq='s')
    # Background flux
    solexs = np.ones(100) * 1e-7
    helios = np.ones(100) * 1e-8
    
    # Introduce a massive flare spike at index 50
    solexs[50:60] = 1e-4
    helios[50:60] = 1e-5
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'solexs_flux': solexs,
        'helios_flux': helios
    })
    
    df_out, cat = detect_flares(df)
    
    assert not df_out.empty
    assert 'flare_active' in df_out.columns
    # Flare should be active during the spike
    assert df_out.loc[55, 'flare_active'] == True
    
    # Catalogue should record the event
    assert not cat.empty
    assert len(cat) == 1
    assert cat.iloc[0]['flare_class'] != 'Unknown'
