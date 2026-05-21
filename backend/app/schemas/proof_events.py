from pydantic import BaseModel, Field


class ProofEventCreate(BaseModel):
    transport_job_id: str
    event_type: str = Field(pattern="^(PICKUP|DELIVERY)$")
    qr_code: str = Field(min_length=8, max_length=128)
    photo_url: str | None = None
    signature_url: str | None = None
    latitude: float
    longitude: float
    notes: str | None = Field(default=None, max_length=500)
