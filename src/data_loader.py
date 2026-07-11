import pandas as pd
import numpy as np
import os

def generate_simulated_data(output_dir='data', duration_hours=24, freq='1S'):
    """
    Generate simulated SoLEXS (Soft X-ray) and HEL1OS (Hard X-ray) data.
    Simulates a background flux with occasional spikes (solar flares).
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a time index
    time_index = pd.date_range(start='2024-01-01 00:00:00', periods=duration_hours*3600, freq=freq)
    n_samples = len(time_index)
    
    # Base background noise
    solexs_base = np.random.normal(loc=1e-7, scale=1e-8, size=n_samples)
    helios_base = np.random.normal(loc=1e-8, scale=2e-9, size=n_samples)
    
    solexs_flux = np.abs(solexs_base)
    helios_flux = np.abs(helios_base)
    
    # Simulate flares
    num_flares = 10
    flare_indices = np.random.choice(n_samples - 600, size=num_flares, replace=False)
    
    for idx in flare_indices:
        # Flare characteristics
        flare_class = np.random.choice(['C', 'M', 'X'], p=[0.7, 0.2, 0.1])
        if flare_class == 'C':
            multiplier = np.random.uniform(10, 50)
        elif flare_class == 'M':
            multiplier = np.random.uniform(50, 500)
        else: # X class
            multiplier = np.random.uniform(500, 5000)
            
        flare_duration = np.random.randint(60, 600) # 1 to 10 minutes
        
        # Soft X-ray (SoLEXS) usually peaks slower and lasts longer
        x_soft = np.linspace(0, np.pi, flare_duration)
        flare_profile_soft = np.sin(x_soft) ** 2 * (1e-7 * multiplier)
        
        # Hard X-ray (HEL1OS) peaks earlier and sharper (impulsive phase)
        flare_duration_hard = int(flare_duration * 0.6)
        x_hard = np.linspace(0, np.pi, flare_duration_hard)
        flare_profile_hard = np.sin(x_hard) ** 4 * (1e-8 * multiplier * 0.5)
        
        # Add to flux
        end_idx_soft = min(idx + flare_duration, n_samples)
        solexs_flux[idx:end_idx_soft] += flare_profile_soft[:end_idx_soft-idx]
        
        end_idx_hard = min(idx + flare_duration_hard, n_samples)
        helios_flux[idx:end_idx_hard] += flare_profile_hard[:end_idx_hard-idx]
        
    # Create DataFrames
    df_solexs = pd.DataFrame({'timestamp': time_index, 'solexs_flux': solexs_flux})
    df_helios = pd.DataFrame({'timestamp': time_index, 'helios_flux': helios_flux})
    
    # Save to CSV
    solexs_path = os.path.join(output_dir, 'solexs_simulated.csv')
    helios_path = os.path.join(output_dir, 'helios_simulated.csv')
    df_solexs.to_csv(solexs_path, index=False)
    df_helios.to_csv(helios_path, index=False)
    
    print(f"Simulated data generated at {output_dir}")
    return solexs_path, helios_path

def load_and_merge_data(solexs_path, helios_path):
    """
    Load SoLEXS and HEL1OS CSVs and merge them on timestamp.
    """
    df_solexs = pd.read_csv(solexs_path)
    df_helios = pd.read_csv(helios_path)
    
    df_solexs['timestamp'] = pd.to_datetime(df_solexs['timestamp'])
    df_helios['timestamp'] = pd.to_datetime(df_helios['timestamp'])
    
    # Merge as of or exact match (assuming exact match for simulated)
    df_merged = pd.merge(df_solexs, df_helios, on='timestamp', how='outer')
    df_merged = df_merged.sort_values('timestamp').reset_index(drop=True)
    
    # Forward fill missing values if any
    df_merged = df_merged.ffill().bfill()
    
    return df_merged

if __name__ == "__main__":
    generate_simulated_data()
