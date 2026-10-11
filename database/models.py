from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from database.database import Base


class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    language = Column(String, default="English")
    created_at = Column(DateTime, default=datetime.utcnow)


class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, nullable=False)
    farm_name = Column(String, nullable=False)
    area = Column(Float, nullable=False)
    area_unit = Column(String, default="sqft")
    soil_type = Column(String, nullable=True)
    soil_ph = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, nullable=True)
    farm_id = Column(Integer, nullable=True)
    crop = Column(String, nullable=False)
    crop_year = Column(Integer, nullable=True)
    season = Column(String, nullable=True)
    state = Column(String, nullable=True)
    area = Column(Float, nullable=True)
    rainfall = Column(Float, nullable=True)
    fertilizer = Column(Float, nullable=True)
    pesticide = Column(Float, nullable=True)
    predicted_yield = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)