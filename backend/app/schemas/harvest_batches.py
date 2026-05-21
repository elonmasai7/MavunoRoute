from datetime import datetime

from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import HarvestBatchStatus
from app.schemas.common import BaseReadSchema


class HarvestBatchCreate(BaseModel):
    farmer_id: str
    crop_id: str
    quantity_kg: float = Field(gt=0)
    expected_harvest_datetime: datetime
    grade: str = Field(min_length=1, max_length=64)
    packaging_type: str = Field(min_length=1, max_length=64)
    asking_price_per_kg: float = Field(gt=0)
    latitude: float
    longitude: float


class HarvestBatchUpdate(BaseModel):
    quantity_kg: float | None = Field(default=None, gt=0)
    expected_harvest_datetime: datetime | None = None
    actual_harvest_datetime: datetime | None = None
    grade: str | None = Field(default=None, min_length=1, max_length=64)
    packaging_type: str | None = Field(default=None, min_length=1, max_length=64)
    asking_price_per_kg: float | None = Field(default=None, gt=0)
    status: HarvestBatchStatus | None = None


class HarvestBatchRead(BaseReadSchema):
    farmer_id: UUID
    crop_id: UUID
    quantity_kg: float
    expected_harvest_datetime: datetime
    actual_harvest_datetime: datetime | None
    grade: str
    packaging_type: str
    asking_price_per_kg: float
    latitude: float
    longitude: float
    status: HarvestBatchStatus
    spoilage_risk_score: int
