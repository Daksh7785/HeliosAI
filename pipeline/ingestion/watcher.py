import os
import time
import glob
import pandas as pd
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))
from app.models.schema import RawLightCurve

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://helios:helios_password@localhost:5432/helios_db")
RAW_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/raw'))
PROCESSED_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/processed'))

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class LightCurveRecord(BaseModel):
    timestamp: str
    instrument: str
    energy_band: str
    counts: float
    error: float | None = None

def process_file(filepath):
    print(f"Processing file: {filepath}")
    try:
        df = pd.read_csv(filepath)
        records = df.to_dict(orient="records")
        valid_records = []
        
        for record in records:
            try:
                validated = LightCurveRecord(**record)
                valid_records.append(
                    RawLightCurve(
                        timestamp=pd.to_datetime(validated.timestamp),
                        instrument=validated.instrument,
                        energy_band=validated.energy_band,
                        counts=validated.counts,
                        error=validated.error
                    )
                )
            except ValidationError as e:
                print(f"Validation error in record: {e}")
        
        if valid_records:
            with SessionLocal() as session:
                session.add_all(valid_records)
                session.commit()
                print(f"Inserted {len(valid_records)} records into db.")
        
        # Move to processed
        os.rename(filepath, os.path.join(PROCESSED_DATA_DIR, os.path.basename(filepath)))
        print(f"Moved {filepath} to processed.")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def watch_directory():
    print(f"Watching directory {RAW_DATA_DIR} for new CSV files...")
    while True:
        csv_files = glob.glob(os.path.join(RAW_DATA_DIR, "*.csv"))
        for file in csv_files:
            process_file(file)
        time.sleep(10)

if __name__ == "__main__":
    watch_directory()
