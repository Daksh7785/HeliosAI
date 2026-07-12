from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Integer, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class RawTelemetry(Base):
    __tablename__ = "raw_telemetry"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    instrument = Column(String, nullable=False, index=True) # "SoLEXS" or "HEL1OS"
    energy_band = Column(String, nullable=False)
    flux = Column(Float, nullable=False)
    ingested_at = Column(DateTime, default=datetime.utcnow)

class FeatureStore(Base):
    __tablename__ = "feature_store"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, unique=True, index=True)
    solexs_flux = Column(Float, nullable=False)
    hel1os_flux = Column(Float, nullable=False)
    hardness_ratio = Column(Float, nullable=False)
    is_flare_candidate = Column(Boolean, default=False)
    forecast_probability = Column(Float, nullable=True) # Added for forecasting
    xai_top_features = Column(String, nullable=True) # JSON array of top contributing features
    data_quality_flag = Column(String, default="RAW") # "RAW", "VALIDATED", "QUARANTINED"
    processed_at = Column(DateTime, default=datetime.utcnow)

class FlareCatalogue(Base):
    __tablename__ = "flare_catalogue"
    
    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, nullable=False, index=True)
    peak_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    class_level = Column(String, nullable=True) # e.g., "M1.2"
    peak_flux = Column(Float, nullable=False)
    source = Column(String, nullable=False) # e.g., "HeliosAI-Nowcast"
    created_at = Column(DateTime, default=datetime.utcnow)
