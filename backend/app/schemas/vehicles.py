from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import BaseReadSchema


class VehicleCreate(BaseModel):
    transporter_id: str
    plate_number: str = Field(min_length=3, max_length=32)
    vehicle_type: str = Field(min_length=2, max_length=64)
    capacity_kg: float = Field(gt=0)
    has_refrigeration: bool
    temperature_min: float | None = None
    temperature_max: float | None = None
    insurance_status: str = Field(min_length=2, max_length=64)
    inspection_status: str = Field(min_length=2, max_length=64)


class VehicleUpdate(BaseModel):
    vehicle_type: str | None = Field(default=None, min_length=2, max_length=64)
    capacity_kg: float | None = Field(default=None, gt=0)
    has_refrigeration: bool | None = None
    temperature_min: float | None = None
    temperature_max: float | None = None
    insurance_status: str | None = Field(default=None, min_length=2, max_length=64)
    inspection_status: str | None = Field(default=None, min_length=2, max_length=64)
    is_available: bool | None = None


class VehicleAvailabilityUpdate(BaseModel):
    is_available: bool


class VehicleRead(BaseReadSchema):
    transporter_id: UUID
    plate_number: str
    vehicle_type: str
    capacity_kg: float
    has_refrigeration: bool
    temperature_min: float | None
    temperature_max: float | None
    insurance_status: str
    inspection_status: str
    is_available: bool
