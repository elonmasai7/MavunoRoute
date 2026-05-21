from datetime import datetime

from pydantic import BaseModel, Field


class NotificationSendRequest(BaseModel):
    user_id: str
    channel: str = Field(min_length=2, max_length=32)
    subject: str = Field(min_length=2, max_length=255)
    message: str = Field(min_length=2, max_length=500)


class NotificationRead(BaseModel):
    id: str
    user_id: str
    channel: str
    subject: str
    message: str
    provider: str
    status: str
    provider_reference: str | None
    created_at: datetime
