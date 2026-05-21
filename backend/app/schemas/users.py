from pydantic import BaseModel, EmailStr, Field

from app.models.enums import UserRole
from app.schemas.common import BaseReadSchema


class UserRead(BaseReadSchema):
    full_name: str
    email: EmailStr
    phone_number: str
    role: UserRole
    is_active: bool
    is_verified: bool


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=255)
    phone_number: str | None = Field(default=None, min_length=10, max_length=32)
    is_verified: bool | None = None
