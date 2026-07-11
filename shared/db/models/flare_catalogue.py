from sqlalchemy import Column, String, Float, DateTime, Index
from shared.db.models.raw_light_curve import Base

class FlareCatalogue(Base):
    __tablename__ = "flare_catalogue"
    
    event_id = Column(String, primary_key=True)
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    peak_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    
    goes_class = Column(String, nullable=False, index=True)
    peak_flux_solexs = Column(Float, nullable=False)
    peak_flux_hel1os = Column(Float, nullable=True)
    
    confidence = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="active")

    __table_args__ = (
        Index('idx_catalogue_start_time', 'start_time'),
    )
