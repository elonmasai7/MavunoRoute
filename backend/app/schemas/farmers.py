from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import VerificationStatus
from app.schemas.common import BaseReadSchema


class FarmerCreate(BaseModel):
    user_id: str
    national_id_hash: str | None = None
    county: str
    sub_county: str
    ward: str
    village: str
    latitude: float
    longitude: float
    cooperative_id: str | None = None
    farm_size_acres: float = Field(gt=0)
    primary_crops: list[str] = Field(default_factory=list)


class FarmerUpdate(BaseModel):
    county: str | None = None
    sub_county: str | None = None
    ward: str | None = None
    village: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    farm_size_acres: float | None = Field(default=None, gt=0)
    primary_crops: list[str] | None = None
    verification_status: VerificationStatus | None = None


class FarmerRead(BaseReadSchema):
    user_id: UUID
    county: str
    sub_county: str
    ward: str
    village: str
    latitude: float
    longitude: float
    cooperative_id: UUID | None
    farm_size_acres: float
    primary_crops: list[str]
    verification_status: VerificationStatus
