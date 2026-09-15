from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class WeatherDataCreate(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    temperature: float
    humidity: float
    pressure: float
    wind_speed: float
    wind_direction: float
    precipitation: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class WeatherData(WeatherDataCreate):
    id: str
    
    class Config:
        from_attributes = True

class WeatherHistoricalQuery(BaseModel):
    latitude: float
    longitude: float
    start_date: datetime
    end_date: datetime
