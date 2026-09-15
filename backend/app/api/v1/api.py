from fastapi import APIRouter
from app.api.v1.endpoints import auth, weather, gis, alerts, analytics, predictions

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])
api_router.include_router(gis.router, prefix="/gis", tags=["gis"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"])
