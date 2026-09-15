from typing import Any, List
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from supabase import Client

from app.api import deps
from app.services.weather_service import WeatherService

router = APIRouter()

class RiskZone(BaseModel):
    latitude: float
    longitude: float
    radius_km: float
    risk_score: float

@router.get("/risk-radius", response_model=List[dict])
def get_locations_in_risk_radius(
    lat: float = Query(..., description="Center latitude"),
    lon: float = Query(..., description="Center longitude"),
    radius_km: float = Query(..., description="Radius in kilometers"),
    db: Client = Depends(deps.get_db),
) -> Any:
    """
    Get all tracked vulnerable locations within a certain radius.
    Ideally implemented via PostGIS using Supabase RPC.
    """
    # Mock implementation until PostGIS RPC is set up
    # Real implementation: return db.rpc("get_locations_in_radius", {"lat": lat, "lon": lon, "radius": radius_km}).execute().data
    return [
        {"location": "Downtown", "distance_km": 2.5, "vulnerability_index": 0.8},
        {"location": "River District", "distance_km": 4.1, "vulnerability_index": 0.95}
    ]
