from datetime import datetime

from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import RouteStatus
from app.schemas.common import BaseReadSchema


class RoutePlanCreate(BaseModel):
    harvest_batch_ids: list[str] = Field(min_length=1)
    destination_buyer_id: str | None = None
    destination_cold_hub_id: str | None = None
    vehicle_id: str | None = None


class RouteStopInput(BaseModel):
    stop_type: str
    sequence_number: int = Field(gt=0)
    latitude: float
    longitude: float
    planned_arrival_time: datetime
    harvest_batch_id: str | None = None
    farmer_id: str | None = None
    buyer_id: str | None = None
    cold_hub_id: str | None = None


class RouteRead(BaseReadSchema):
    route_code: str
    origin_county: str
    destination_county: str
    vehicle_id: UUID | None
    transporter_id: UUID | None
    assigned_driver_id: UUID | None
    total_distance_km: float
    estimated_duration_minutes: int
    route_polyline: str | None
    route_provider: str
    status: RouteStatus
