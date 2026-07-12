import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestion.data_ingestor import main as ingest_main
from src.processing.processor import synchronize_and_extract_features
from src.intelligence.nowcast.detector import ThresholdDetector
from src.shared.database.db import async_session_maker, init_db
from src.shared.database.models import FeatureStore, FlareCatalogue
from sqlalchemy import select

async def run_nowcast():
    print("Running Nowcast detector on feature store...")
    async with async_session_maker() as session:
        # Fetch feature store
        result = await session.execute(select(FeatureStore).order_by(FeatureStore.timestamp))
        records = result.scalars().all()
        
        if not records:
            print("No features to run nowcast on.")
            return
            
        import pandas as pd
        df = pd.DataFrame([{
            'timestamp': r.timestamp,
            'solexs_flux': r.solexs_flux,
            'hel1os_flux': r.hel1os_flux,
            'hardness_ratio': r.hardness_ratio
        } for r in records])
        
        detector = ThresholdDetector(hardness_threshold=0.5, consecutive_points=3)
        events_df = detector.predict(df)
        
        if events_df.empty:
            print("No flares detected by baseline model.")
            return
            
        print(f"Detected {len(events_df)} flare events. Saving to catalogue...")
        
        # Clear existing catalogue for MVP testing simplicity
        await session.execute(FlareCatalogue.__table__.delete())
        
        catalogue_records = []
        for _, row in events_df.iterrows():
            record = FlareCatalogue(
                start_time=row['start_time'],
                peak_time=row['peak_time'],
                end_time=row['end_time'],
                class_level=row['class_level'],
                peak_flux=row['peak_flux'],
                source=row['source']
            )
            catalogue_records.append(record)
            
        session.add_all(catalogue_records)
        await session.commit()
        print("Catalogue updated.")

async def main():
    print("Initializing Database...")
    await init_db()
    
    print("\n--- Pipeline Step 1: Ingestion ---")
    await ingest_main()
    
    print("\n--- Pipeline Step 2: Processing ---")
    await synchronize_and_extract_features()
    
    print("\n--- Pipeline Step 3: Intelligence (Nowcast) ---")
    await run_nowcast()
    
    print("\nPipeline execution complete.")

if __name__ == "__main__":
    asyncio.run(main())
