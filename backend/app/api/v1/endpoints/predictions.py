from typing import Any
from fastapi import APIRouter, Depends

from app.schemas.weather import WeatherDataCreate
from app.ml.model import ml_model

router = APIRouter()

@router.post("/nowcast")
def get_nowcast_prediction(
    data_in: WeatherDataCreate,
) -> Any:
    """
    Get a nowcasting prediction based on current weather data.
    """
    prediction = ml_model.predict_risk(data_in)
    return prediction
