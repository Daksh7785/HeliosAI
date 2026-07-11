from sqlalchemy import Column, String, Float, DateTime, Integer, Index, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# --- Time-Series Tables (To be converted to TimescaleDB Hypertables) ---

class RawRecord(Base):
    """
    Grain: Per validated raw sample, per payload
    """
    __tablename__ = 'raw_records'
    
    spacecraft_ts = Column(DateTime(timezone=True), primary_key=True)
    payload = Column(String, primary_key=True)
    raw_value = Column(Float, nullable=False)
    ingestion_batch_id = Column(String, nullable=False)

    __table_args__ = (
        Index('idx_raw_payload_ts', 'payload', 'spacecraft_ts'),
    )

class FusedSeries(Base):
    """
    Grain: Per common-time-grid point (post Data Synchronization)
    """
    __tablename__ = 'fused_series'
    
    utc_ts = Column(DateTime(timezone=True), primary_key=True)
    solexs_flux = Column(Float, nullable=True)
    hel1os_flux = Column(Float, nullable=True)
    quality_flags = Column(Integer, default=0)

    __table_args__ = (
        Index('idx_fused_utc_ts', 'utc_ts'),
    )

class Feature(Base):
    """
    Grain: Per timestamp, per feature-version
    """
    __tablename__ = 'features'
    
    utc_ts = Column(DateTime(timezone=True), primary_key=True)
    feature_name = Column(String, primary_key=True)
    feature_version = Column(String, primary_key=True)
    value = Column(Float, nullable=False)

    __table_args__ = (
        Index('idx_features_utc_ts', 'utc_ts'),
    )

# --- Conventional Relational Tables ---

class ModelRegistryRef(Base):
    """
    Grain: Per MLflow run
    """
    __tablename__ = 'model_registry_ref'
    
    run_id = Column(String, primary_key=True)
    model_type = Column(String, nullable=False)
    feature_version = Column(String, nullable=False)
    metrics_snapshot = Column(JSON, nullable=True)

class NowcastEvent(Base):
    """
    Grain: Per detected candidate/promoted event
    """
    __tablename__ = 'nowcast_events'
    
    event_id = Column(String, primary_key=True)
    onset_ts = Column(DateTime(timezone=True), nullable=False)
    peak_ts = Column(DateTime(timezone=True), nullable=False)
    flare_class = Column(String, name="class", nullable=False)
    confidence = Column(String, nullable=False)
    status = Column(String, nullable=False)  # promoted or tentative

    __table_args__ = (
        Index('idx_nowcast_status_class', 'status', 'class'),
    )

class Forecast(Base):
    """
    Grain: Per prediction
    """
    __tablename__ = 'forecasts'
    
    forecast_id = Column(String, primary_key=True)
    predicted_trigger_ts = Column(DateTime(timezone=True), nullable=False)
    horizon_minutes = Column(Integer, nullable=False)
    probability = Column(Float, nullable=False)
    class_probs = Column(JSON, nullable=True)
    model_version = Column(String, nullable=False)

class LeadTimeMetric(Base):
    """
    Grain: Per matched forecast <-> event pair
    """
    __tablename__ = 'lead_time_metrics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    forecast_id = Column(String, ForeignKey('forecasts.forecast_id'), nullable=False)
    event_id = Column(String, ForeignKey('nowcast_events.event_id'), nullable=False)
    lead_time_seconds = Column(Float, nullable=False)
