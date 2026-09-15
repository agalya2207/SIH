from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from supabase import Client

from app.api import deps
from app.schemas.user import User
from app.schemas.weather import WeatherDataCreate, WeatherData
from app.services.weather_service import WeatherService

router = APIRouter()

@router.post("/ingest", response_model=WeatherData)
def ingest_weather_data(
    *,
    db: Client = Depends(deps.get_db),
    data_in: WeatherDataCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Ingest new real-time weather data.
    Requires authentication (can be restricted to Authority/Admin).
    """
    if current_user.role not in ["Admin", "Authority"]:
        raise HTTPException(status_code=403, detail="Not enough privileges")
        
    weather_service = WeatherService(db)
    new_data = weather_service.ingest_weather_data(data_in)
    
    if not new_data:
        raise HTTPException(status_code=500, detail="Failed to ingest data")
        
    return WeatherData(**new_data)

@router.get("/historical", response_model=List[WeatherData])
def get_historical_weather(
    lat: float,
    lon: float,
    limit: int = 100,
    db: Client = Depends(deps.get_db),
) -> Any:
    """
    Retrieve historical weather data for a specific location.
    """
    weather_service = WeatherService(db)
    data = weather_service.get_historical_data(lat, lon, limit)
    return data
