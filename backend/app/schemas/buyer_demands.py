from datetime import datetime

from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import BuyerDemandStatus
from app.schemas.common import BaseReadSchema


class BuyerDemandCreate(BaseModel):
    buyer_id: str
    crop_id: str
    quantity_kg: float = Field(gt=0)
    desired_grade: str = Field(min_length=1, max_length=64)
    max_price_per_kg: float = Field(gt=0)
    required_delivery_datetime: datetime
    delivery_latitude: float
    delivery_longitude: float


class BuyerDemandUpdate(BaseModel):
    quantity_kg: float | None = Field(default=None, gt=0)
    desired_grade: str | None = Field(default=None, min_length=1, max_length=64)
    max_price_per_kg: float | None = Field(default=None, gt=0)
    required_delivery_datetime: datetime | None = None
    status: BuyerDemandStatus | None = None


class BuyerDemandRead(BaseReadSchema):
    buyer_id: UUID
    crop_id: UUID
    quantity_kg: float
    desired_grade: str
    max_price_per_kg: float
    required_delivery_datetime: datetime
    delivery_latitude: float
    delivery_longitude: float
    status: BuyerDemandStatus
