from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def get_analytics_health():
    """Analytics endpoint health check"""
    return {"status": "ok", "module": "analytics"}
