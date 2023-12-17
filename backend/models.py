from sqlalchemy import Column, Float, String, Integer
from pydantic import BaseModel

from database import Base

class WeatherDataModel(Base):
    __tablename__ = "weather_data"
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    season = Column(String)
    # Add other fields like 'time'

# Pydantic model for request/response
class WeatherData(BaseModel):
    temperature: float
    humidity: float
    season: str
    # Add other fields like 'time'
