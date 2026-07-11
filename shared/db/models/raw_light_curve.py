from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RawLightCurve(Base):
    __tablename__ = "raw_light_curves"
    
    # Using TimescaleDB, so we typically index heavily on timestamp
    timestamp = Column(DateTime(timezone=True), primary_key=True, index=True)
    instrument = Column(String, primary_key=True, index=True) # solexs or hel1os
    energy_band = Column(String, primary_key=True)
    
    flux = Column(Float, nullable=False)
    quality_flag = Column(Integer, default=0)

    # Creating a composite index for fast querying
    __table_args__ = (
        Index('idx_raw_lc_time_inst', 'timestamp', 'instrument'),
    )
