from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from shared.db.models.raw_light_curve import Base

class ProcessedLightCurve(Base):
    __tablename__ = "processed_light_curves"
    
    timestamp = Column(DateTime(timezone=True), primary_key=True, index=True)
    instrument = Column(String, primary_key=True, index=True)
    energy_band = Column(String, primary_key=True)
    
    flux = Column(Float, nullable=False)
    flux_raw = Column(Float, nullable=False)
    background_level = Column(Float, nullable=False)

    __table_args__ = (
        Index('idx_proc_lc_time_inst', 'timestamp', 'instrument'),
    )
