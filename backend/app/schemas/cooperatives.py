from pydantic import BaseModel, Field

from app.schemas.common import BaseReadSchema


class CooperativeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    registration_number: str = Field(min_length=2, max_length=128)
    county: str = Field(min_length=2, max_length=128)
    contact_person: str = Field(min_length=2, max_length=255)
    phone_number: str = Field(min_length=10, max_length=32)
    latitude: float
    longitude: float


class CooperativeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    county: str | None = Field(default=None, min_length=2, max_length=128)
    contact_person: str | None = Field(default=None, min_length=2, max_length=255)
    phone_number: str | None = Field(default=None, min_length=10, max_length=32)
    latitude: float | None = None
    longitude: float | None = None


class CooperativeRead(BaseReadSchema):
    name: str
    registration_number: str
    county: str
    contact_person: str
    phone_number: str
    latitude: float
    longitude: float
