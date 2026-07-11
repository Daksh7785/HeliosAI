import pandas as pd
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
from app.models.schema import RawLightCurve, EngineeredFeature

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://helios:helios_password@localhost:5432/helios_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def fetch_raw_data(minutes=60):
    """Fetch recent raw data from DB."""
    query = f"""
    SELECT * FROM raw_light_curves 
    WHERE timestamp >= NOW() - INTERVAL '{minutes} minutes'
    ORDER BY timestamp ASC
    """
    df = pd.read_sql(query, con=engine)
    return df

def subtract_background(df, window=50):
    """Simple moving average background subtraction."""
    df['bg'] = df.groupby(['instrument', 'energy_band'])['counts'].transform(lambda x: x.rolling(window, min_periods=1).mean())
    df['counts_subtracted'] = df['counts'] - df['bg']
    df.loc[df['counts_subtracted'] < 0, 'counts_subtracted'] = 0
    return df

def sync_and_engineer_features(df):
    """Sync time, compute derivative, hardness ratio."""
    if df.empty:
        return pd.DataFrame()
        
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Pivot for cross-band calculations
    pivoted = df.pivot_table(
        index='timestamp', 
        columns=['instrument', 'energy_band'], 
        values='counts_subtracted'
    ).resample('1S').mean().interpolate(method='linear')
    
    features = pd.DataFrame(index=pivoted.index)
    
    # Compute Hardness Ratio if both soft (SoLEXS) and hard (HEL1OS) are present
    if ('SoLEXS', 'soft') in pivoted.columns and ('HEL1OS', 'hard') in pivoted.columns:
        soft = pivoted[('SoLEXS', 'soft')]
        hard = pivoted[('HEL1OS', 'hard')]
        features['hardness_ratio'] = hard / (soft + 1e-5)
    else:
        features['hardness_ratio'] = np.nan
        
    # Calculate derivative on a representative band (e.g. SoLEXS soft)
    if ('SoLEXS', 'soft') in pivoted.columns:
        features['derivative'] = pivoted[('SoLEXS', 'soft')].diff()
        
    # Calculate rolling MAD (Median Absolute Deviation)
    if ('SoLEXS', 'soft') in pivoted.columns:
        rolling_median = pivoted[('SoLEXS', 'soft')].rolling(60).median()
        features['rolling_mad'] = abs(pivoted[('SoLEXS', 'soft')] - rolling_median)
        
    return features.reset_index()

def run_processing():
    print("Running processing pipeline...")
    df = fetch_raw_data()
    if df.empty:
        print("No new data to process.")
        return
        
    df_sub = subtract_background(df)
    features_df = sync_and_engineer_features(df_sub)
    
    if not features_df.empty:
        records = features_df.to_dict(orient='records')
        db_records = []
        for r in records:
            db_records.append(
                EngineeredFeature(
                    timestamp=r['timestamp'],
                    hardness_ratio=r.get('hardness_ratio'),
                    derivative=r.get('derivative'),
                    rolling_mad=r.get('rolling_mad')
                )
            )
        
        with SessionLocal() as session:
            session.add_all(db_records)
            session.commit()
            print(f"Inserted {len(db_records)} engineered features.")
            
if __name__ == "__main__":
    run_processing()
