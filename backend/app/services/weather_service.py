import httpx

from fastapi import HTTPException, status

from app.config import get_settings

settings = get_settings()


class WeatherService:
    @staticmethod
    def _ensure_configured() -> None:
        if not settings.openweather_api_key:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Weather provider not configured")

    async def get_current_temperature(self, latitude: float, longitude: float) -> float | None:
        if not settings.openweather_api_key:
            return None

        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": settings.openweather_api_key,
            "units": "metric",
        }
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get("https://api.openweathermap.org/data/2.5/weather", params=params)
            response.raise_for_status()
            payload = response.json()
            return payload.get("main", {}).get("temp")

    async def current(self, latitude: float, longitude: float) -> dict:
        self._ensure_configured()
        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": settings.openweather_api_key,
            "units": "metric",
        }
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get("https://api.openweathermap.org/data/2.5/weather", params=params)
            response.raise_for_status()
            payload = response.json()
            return {
                "latitude": latitude,
                "longitude": longitude,
                "temperature_celsius": payload.get("main", {}).get("temp"),
                "humidity": payload.get("main", {}).get("humidity"),
                "condition": payload.get("weather", [{}])[0].get("description"),
            }

    async def forecast(self, latitude: float, longitude: float) -> dict:
        self._ensure_configured()
        params = {"lat": latitude, "lon": longitude, "appid": settings.openweather_api_key, "units": "metric"}
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get("https://api.openweathermap.org/data/2.5/forecast", params=params)
            response.raise_for_status()
            payload = response.json()
            sample = payload.get("list", [])[:5]
            return {
                "latitude": latitude,
                "longitude": longitude,
                "forecast": [
                    {
                        "datetime": item.get("dt_txt"),
                        "temperature_celsius": item.get("main", {}).get("temp"),
                        "humidity": item.get("main", {}).get("humidity"),
                    }
                    for item in sample
                ],
            }

    async def route_risk(self, start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> dict:
        start = await self.current(start_lat, start_lon)
        end = await self.current(end_lat, end_lon)
        max_temp = max(start["temperature_celsius"] or 0, end["temperature_celsius"] or 0)
        risk_level = "LOW"
        if max_temp >= 30:
            risk_level = "HIGH"
        elif max_temp >= 24:
            risk_level = "MEDIUM"
        return {
            "start": start,
            "end": end,
            "risk_level": risk_level,
            "max_temperature_celsius": max_temp,
        }
