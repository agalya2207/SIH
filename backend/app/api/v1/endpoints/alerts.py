from typing import Any, List
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from supabase import Client

from app.api import deps
from app.schemas.alert import Alert, AlertCreate
from app.schemas.user import User

router = APIRouter()

@router.post("/", response_model=Alert)
def create_alert(
    *,
    db: Client = Depends(deps.get_db),
    alert_in: AlertCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new weather alert.
    Requires Authority or Admin role.
    """
    if current_user.role not in ["Admin", "Authority"]:
        raise HTTPException(status_code=403, detail="Not authorized to create alerts")
        
    alert_data = alert_in.model_dump()
    alert_data["id"] = str(uuid.uuid4())
    alert_data["created_at"] = datetime.utcnow().isoformat()
    alert_data["is_active"] = True
    
    try:
        response = db.table("alerts").insert(alert_data).execute()
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=500, detail="Error saving alert to DB")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/active", response_model=List[Alert])
def get_active_alerts(
    db: Client = Depends(deps.get_db),
) -> Any:
    """
    Get all active alerts. Public endpoint.
    """
    try:
        response = db.table("alerts").select("*").eq("is_active", True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Error fetching alerts: {e}")
        return []
