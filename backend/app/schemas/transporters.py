from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import VerificationStatus
from app.schemas.common import BaseReadSchema


class TransporterCreate(BaseModel):
    user_id: str
    business_name: str = Field(min_length=2, max_length=255)
    license_number: str = Field(min_length=4, max_length=128)
    phone_number: str = Field(min_length=10, max_length=32)
    county: str = Field(min_length=2, max_length=128)


class TransporterUpdate(BaseModel):
    business_name: str | None = Field(default=None, min_length=2, max_length=255)
    phone_number: str | None = Field(default=None, min_length=10, max_length=32)
    county: str | None = Field(default=None, min_length=2, max_length=128)
    verification_status: VerificationStatus | None = None
    rating: float | None = Field(default=None, ge=0)


class TransporterRead(BaseReadSchema):
    user_id: UUID
    business_name: str
    license_number: str
    phone_number: str
    county: str
    verification_status: VerificationStatus
    rating: float
