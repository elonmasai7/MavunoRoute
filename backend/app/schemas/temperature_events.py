from datetime import datetime

from pydantic import BaseModel, Field


class TemperatureEventCreate(BaseModel):
    harvest_batch_id: str
    transport_job_id: str | None = None
    cold_hub_id: str | None = None
    temperature_celsius: float
    humidity: float | None = None
    source: str = Field(min_length=2, max_length=64)
    recorded_at: datetime | None = None
