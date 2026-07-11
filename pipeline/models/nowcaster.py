import pandas as pd
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import sys
import uuid
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
from app.models.schema import EngineeredFeature, FlareCatalogue

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://helios:helios_password@localhost:5432/helios_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def detect_flares(window_minutes=60, threshold_sigma=3.0):
    print("Running Nowcasting Detection...")
    query = f"""
    SELECT * FROM engineered_features 
    WHERE timestamp >= NOW() - INTERVAL '{window_minutes} minutes'
    ORDER BY timestamp ASC
    """
    df = pd.read_sql(query, con=engine)
    if df.empty or 'rolling_mad' not in df.columns:
        print("Not enough engineered features for nowcasting.")
        return

    # Detection logic based on rolling MAD threshold
    df['is_flare'] = df['rolling_mad'] > (threshold_sigma * df['rolling_mad'].median())
    
    # Simple event boundary grouping
    df['event_group'] = (df['is_flare'] != df['is_flare'].shift()).cumsum()
    events = df[df['is_flare']].groupby('event_group')
    
    catalog_entries = []
    for _, event_data in events:
        if len(event_data) < 5:
            continue # Ignore micro-spikes (less than 5 seconds)
            
        start_time = event_data['timestamp'].min()
        end_time = event_data['timestamp'].max()
        peak_idx = event_data['rolling_mad'].idxmax()
        peak_time = event_data.loc[peak_idx, 'timestamp']
        peak_flux = event_data.loc[peak_idx, 'rolling_mad']
        
        # Simple GOES class estimation heuristic (placeholder)
        goes_class = "C" if peak_flux < 100 else ("M" if peak_flux < 1000 else "X")
        
        flare_id = f"FLARE-{start_time.strftime('%Y%m%d-%H%M%S')}"
        
        catalog_entries.append(
            FlareCatalogue(
                id=flare_id,
                start_time=start_time,
                peak_time=peak_time,
                end_time=end_time,
                goes_class_estimate=goes_class,
                peak_flux=peak_flux,
                is_verified=False
            )
        )
        
    if catalog_entries:
        with SessionLocal() as session:
            # Check for existing
            existing_ids = [c.id for c in session.query(FlareCatalogue.id).all()]
            new_entries = [c for c in catalog_entries if c.id not in existing_ids]
            if new_entries:
                session.add_all(new_entries)
                session.commit()
                print(f"Detected and cataloged {len(new_entries)} new flares.")
            else:
                print("No new flares to catalog.")
    else:
        print("No flares detected.")

if __name__ == "__main__":
    detect_flares()
