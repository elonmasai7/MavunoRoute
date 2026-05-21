import httpx

from app.providers.weather.base import WeatherProviderInterface


class OpenWeatherProvider(WeatherProviderInterface):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def current_temperature(self, latitude: float, longitude: float) -> float | None:
        params = {"lat": latitude, "lon": longitude, "units": "metric", "appid": self.api_key}
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get("https://api.openweathermap.org/data/2.5/weather", params=params)
            response.raise_for_status()
            return response.json().get("main", {}).get("temp")
