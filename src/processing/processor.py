import asyncio
import pandas as pd
from sqlalchemy import select
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.shared.database.db import async_session_maker
from src.shared.database.models import RawTelemetry, FeatureStore

async def synchronize_and_extract_features():
    print("Starting processing and synchronization...")
    
    async with async_session_maker() as session:
        # Fetch raw data
        result = await session.execute(select(RawTelemetry).order_by(RawTelemetry.timestamp))
        records = result.scalars().all()
        
        if not records:
            print("No raw telemetry found.")
            return
            
        # Convert to pandas for easy time-series alignment
        df = pd.DataFrame([{
            'timestamp': r.timestamp,
            'instrument': r.instrument,
            'flux': r.flux
        } for r in records])
        
        # Pivot to align timestamps
        df_pivot = df.pivot_table(index='timestamp', columns='instrument', values='flux').reset_index()
        
        # Handle cases where one instrument might be missing (forward fill, then fillna with 0)
        df_pivot.ffill(inplace=True)
        df_pivot.fillna(0, inplace=True)
        
        # Calculate hardness ratio
        # Avoid division by zero
        df_pivot['hardness_ratio'] = df_pivot['HEL1OS'] / (df_pivot['SoLEXS'] + 1e-9)
        
        # Identify flare candidates (simple thresholding logic for the processing phase)
        # We will refine this in the intelligence layer
        df_pivot['is_flare_candidate'] = df_pivot['hardness_ratio'] > 0.5
        
        feature_records = []
        for _, row in df_pivot.iterrows():
            record = FeatureStore(
                timestamp=row['timestamp'],
                solexs_flux=row['SoLEXS'],
                hel1os_flux=row['HEL1OS'],
                hardness_ratio=row['hardness_ratio'],
                is_flare_candidate=bool(row['is_flare_candidate'])
            )
            feature_records.append(record)
            
        # Clear existing feature store for simplicity in MVP runs
        # In prod, this would only process new records
        await session.execute(FeatureStore.__table__.delete())
        
        # Bulk insert
        session.add_all(feature_records)
        await session.commit()
        
    print(f"Successfully processed {len(feature_records)} synchronized records into the feature store.")

if __name__ == "__main__":
    asyncio.run(synchronize_and_extract_features())
