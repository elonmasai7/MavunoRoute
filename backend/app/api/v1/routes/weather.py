from fastapi import APIRouter, Depends

from app.dependencies import require_permission
from app.services.weather_service import WeatherService
from app.utils.response import success_response

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("/current")
async def current(latitude: float, longitude: float, _=Depends(require_permission("weather:read"))):
    data = await WeatherService().current(latitude, longitude)
    return success_response("Records retrieved successfully", data)


@router.get("/forecast")
async def forecast(latitude: float, longitude: float, _=Depends(require_permission("weather:read"))):
    data = await WeatherService().forecast(latitude, longitude)
    return success_response("Records retrieved successfully", data)


@router.get("/route-risk")
async def route_risk(
    start_latitude: float,
    start_longitude: float,
    end_latitude: float,
    end_longitude: float,
    _=Depends(require_permission("weather:read")),
):
    data = await WeatherService().route_risk(start_latitude, start_longitude, end_latitude, end_longitude)
    return success_response("Records retrieved successfully", data)
