import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_synthetic_data(output_dir="data/raw"):
    os.makedirs(output_dir, exist_ok=True)
    
    # 2 days of data at 1-second cadence
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=2)
    
    timestamps = pd.date_range(start=start_time, end=end_time, freq='1s')
    n = len(timestamps)
    
    # Simulate background noise
    np.random.seed(42)
    solexs_bg = np.random.normal(10, 2, n)
    hel1os_bg = np.random.normal(2, 0.5, n)
    
    solexs_flux = solexs_bg.copy()
    hel1os_flux = hel1os_bg.copy()
    
    # Inject a few flares
    flare_centers = [
        start_time + timedelta(hours=6),
        start_time + timedelta(hours=18),
        start_time + timedelta(hours=36)
    ]
    
    for center in flare_centers:
        # Distance in seconds from center
        idx_diff = (timestamps - center).total_seconds()
        
        # Simple Gaussian flare shape for soft X-rays (longer decay)
        # SoLEXS sees larger flux
        flare_soft = 500 * np.exp(-0.5 * (idx_diff / 300)**2) 
        
        # Hard X-rays usually peak faster and decay faster, sometimes slightly earlier
        flare_hard = 100 * np.exp(-0.5 * ((idx_diff + 30) / 100)**2)
        
        solexs_flux += flare_soft
        hel1os_flux += flare_hard
        
    df_solexs = pd.DataFrame({'timestamp': timestamps, 'flux': solexs_flux, 'energy_band': '1-30keV'})
    df_hel1os = pd.DataFrame({'timestamp': timestamps, 'flux': hel1os_flux, 'energy_band': '20-150keV'})
    
    # Save to CSV (simulate raw files)
    solexs_path = os.path.join(output_dir, 'solexs_synthetic.csv')
    hel1os_path = os.path.join(output_dir, 'hel1os_synthetic.csv')
    
    df_solexs.to_csv(solexs_path, index=False)
    df_hel1os.to_csv(hel1os_path, index=False)
    
    print(f"Generated synthetic SoLEXS data: {solexs_path}")
    print(f"Generated synthetic HEL1OS data: {hel1os_path}")

if __name__ == "__main__":
    generate_synthetic_data()
