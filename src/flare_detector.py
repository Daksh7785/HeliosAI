import pandas as pd
import numpy as np

def detect_flares(df, soft_col='solexs_flux', hard_col='helios_flux', window=300, threshold_multiplier=5):
    """
    Algorithmic nowcasting of solar flares.
    Uses rolling median and median absolute deviation (MAD) to detect spikes.
    Combines detections from both soft and hard X-rays.
    """
    df = df.copy()
    
    # --- Soft X-ray Detection (SoLEXS) ---
    # Rolling median as baseline
    df['soft_baseline'] = df[soft_col].rolling(window=window, min_periods=1, center=True).median()
    # Rolling MAD for dynamic thresholding
    df['soft_mad'] = df[soft_col].rolling(window=window, min_periods=1, center=True).apply(lambda x: np.median(np.abs(x - np.median(x))), raw=True)
    
    # Soft flare condition: flux > baseline + (threshold * mad) AND must be > 5e-7 (above normal noise floor)
    df['soft_flare_detected'] = (df[soft_col] > (df['soft_baseline'] + threshold_multiplier * df['soft_mad'])) & (df[soft_col] > 5e-7)
    
    # --- Hard X-ray Detection (HEL1OS) ---
    df['hard_baseline'] = df[hard_col].rolling(window=window, min_periods=1, center=True).median()
    df['hard_mad'] = df[hard_col].rolling(window=window, min_periods=1, center=True).apply(lambda x: np.median(np.abs(x - np.median(x))), raw=True)
    
    # Hard flare condition AND must be > 5e-8
    df['hard_flare_detected'] = (df[hard_col] > (df['hard_baseline'] + threshold_multiplier * df['hard_mad'])) & (df[hard_col] > 5e-8)
    
    # --- Master Catalogue (Combined) ---
    # Flare is flagged if either soft or hard detects it. Hard X-ray is usually impulsive and happens earlier.
    df['flare_active'] = df['soft_flare_detected'] | df['hard_flare_detected']
    
    # Standard GOES classification based on peak Soft X-ray flux (W/m^2)
    conditions = [
        df[soft_col] >= 1e-4,
        df[soft_col] >= 1e-5,
        df[soft_col] >= 1e-6,
        df[soft_col] >= 1e-7
    ]
    choices = ['X', 'M', 'C', 'B']
    df['flare_class'] = np.select(conditions, choices, default='A')
    
    # Group contiguous flare active regions to create distinct events
    # identifying start, peak, and end times.
    df['event_group'] = (df['flare_active'] != df['flare_active'].shift()).cumsum()
    flare_events = df[df['flare_active']].groupby('event_group').agg(
        start_time=('timestamp', 'min'),
        end_time=('timestamp', 'max'),
        peak_soft_flux=('solexs_flux', 'max'),
        peak_hard_flux=('helios_flux', 'max'),
    ).reset_index(drop=True)
    
    # Determine class for each event based on peak soft flux
    cond_event = [
        flare_events['peak_soft_flux'] >= 1e-4,
        flare_events['peak_soft_flux'] >= 1e-5,
        flare_events['peak_soft_flux'] >= 1e-6,
        flare_events['peak_soft_flux'] >= 1e-7
    ]
    flare_events['flare_class'] = np.select(cond_event, choices, default='A')
    
    return df, flare_events

if __name__ == "__main__":
    from data_loader import load_and_merge_data
    df = load_and_merge_data('data/solexs_simulated.csv', 'data/helios_simulated.csv')
    df_processed, catalogue = detect_flares(df)
    print("Master Flare Catalogue:")
    print(catalogue)
