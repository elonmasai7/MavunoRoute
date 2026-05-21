from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import BaseReadSchema


class ColdHubCreate(BaseModel):
    operator_id: str
    name: str = Field(min_length=2, max_length=255)
    county: str = Field(min_length=2, max_length=128)
    latitude: float
    longitude: float
    total_capacity_kg: float = Field(gt=0)
    available_capacity_kg: float = Field(ge=0)
    temperature_min: float
    temperature_max: float


class ColdHubUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    county: str | None = Field(default=None, min_length=2, max_length=128)
    total_capacity_kg: float | None = Field(default=None, gt=0)
    available_capacity_kg: float | None = Field(default=None, ge=0)
    temperature_min: float | None = None
    temperature_max: float | None = None
    is_active: bool | None = None


class CapacityUpdate(BaseModel):
    available_capacity_kg: float = Field(ge=0)


class ColdHubRead(BaseReadSchema):
    operator_id: UUID
    name: str
    county: str
    latitude: float
    longitude: float
    total_capacity_kg: float
    available_capacity_kg: float
    temperature_min: float
    temperature_max: float
    is_active: bool
