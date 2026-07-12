import asyncio
import pandas as pd
import sys
import os

# Add src to python path for local execution
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.shared.database.db import async_session_maker
from src.shared.database.models import RawTelemetry

async def ingest_csv(filepath: str, instrument: str):
    print(f"Ingesting {instrument} data from {filepath}...")
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    records = []
    for _, row in df.iterrows():
        record = RawTelemetry(
            timestamp=row['timestamp'],
            instrument=instrument,
            energy_band=row['energy_band'],
            flux=row['flux']
        )
        records.append(record)
        
    # Bulk insert
    async with async_session_maker() as session:
        session.add_all(records)
        await session.commit()
    print(f"Successfully ingested {len(records)} records for {instrument}.")

async def main():
    solexs_path = "data/raw/solexs_synthetic.csv"
    hel1os_path = "data/raw/hel1os_synthetic.csv"
    
    if os.path.exists(solexs_path):
        await ingest_csv(solexs_path, "SoLEXS")
    else:
        print(f"File not found: {solexs_path}")
        
    if os.path.exists(hel1os_path):
        await ingest_csv(hel1os_path, "HEL1OS")
    else:
        print(f"File not found: {hel1os_path}")

if __name__ == "__main__":
    asyncio.run(main())
