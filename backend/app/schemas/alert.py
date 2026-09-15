from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class AlertCreate(BaseModel):
    title: str
    description: str
    severity: str # Low, Moderate, High, Critical
    latitude: float
    longitude: float
    radius_km: float

class Alert(AlertCreate):
    id: str
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True
