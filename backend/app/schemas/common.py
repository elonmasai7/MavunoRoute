from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class APIMessage(BaseModel):
    success: bool
    message: str
    data: dict | list | None = None
    meta: dict | None = None


class ErrorMessage(BaseModel):
    success: bool = False
    message: str
    errors: dict
    code: str


class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 20


class BaseReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
