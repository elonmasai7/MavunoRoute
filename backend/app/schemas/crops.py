from pydantic import BaseModel, Field

from app.schemas.common import BaseReadSchema


class CropCreate(BaseModel):
    name: str = Field(min_length=2, max_length=128)
    category: str = Field(min_length=2, max_length=64)
    perishability_level: int = Field(ge=1, le=10)
    ideal_temperature_min: float
    ideal_temperature_max: float
    shelf_life_hours: int = Field(gt=0)
    handling_notes: str = Field(default="", max_length=500)


class CropUpdate(BaseModel):
    category: str | None = Field(default=None, min_length=2, max_length=64)
    perishability_level: int | None = Field(default=None, ge=1, le=10)
    ideal_temperature_min: float | None = None
    ideal_temperature_max: float | None = None
    shelf_life_hours: int | None = Field(default=None, gt=0)
    handling_notes: str | None = Field(default=None, max_length=500)


class CropRead(BaseReadSchema):
    name: str
    category: str
    perishability_level: int
    ideal_temperature_min: float
    ideal_temperature_max: float
    shelf_life_hours: int
    handling_notes: str
