from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import VerificationStatus
from app.schemas.common import BaseReadSchema


class BuyerCreate(BaseModel):
    user_id: str
    business_name: str = Field(min_length=2, max_length=255)
    business_type: str = Field(min_length=2, max_length=128)
    kra_pin: str | None = Field(default=None, max_length=32)
    county: str = Field(min_length=2, max_length=128)
    delivery_address: str = Field(min_length=2, max_length=255)
    latitude: float
    longitude: float


class BuyerUpdate(BaseModel):
    business_name: str | None = Field(default=None, min_length=2, max_length=255)
    business_type: str | None = Field(default=None, min_length=2, max_length=128)
    kra_pin: str | None = Field(default=None, max_length=32)
    county: str | None = Field(default=None, min_length=2, max_length=128)
    delivery_address: str | None = Field(default=None, min_length=2, max_length=255)
    latitude: float | None = None
    longitude: float | None = None


class BuyerRead(BaseReadSchema):
    user_id: UUID
    business_name: str
    business_type: str
    kra_pin: str | None
    county: str
    delivery_address: str
    latitude: float
    longitude: float
    verification_status: VerificationStatus
