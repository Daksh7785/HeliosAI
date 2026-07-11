from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean
from ..core.database import Base

class RawLightCurve(Base):
    __tablename__ = "raw_light_curves"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True, nullable=False)
    instrument = Column(String, index=True, nullable=False)
    energy_band = Column(String, nullable=False)
    counts = Column(Float, nullable=False)
    error = Column(Float, nullable=True)

class EngineeredFeature(Base):
    __tablename__ = "engineered_features"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True, nullable=False)
    hardness_ratio = Column(Float, nullable=True)
    derivative = Column(Float, nullable=True)
    rolling_mad = Column(Float, nullable=True)

class FlareCatalogue(Base):
    __tablename__ = "flare_catalogue"

    id = Column(String, primary_key=True, index=True)
    start_time = Column(DateTime, nullable=False)
    peak_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    goes_class_estimate = Column(String, nullable=True)
    peak_flux = Column(Float, nullable=False)
    is_verified = Column(Boolean, default=False)
