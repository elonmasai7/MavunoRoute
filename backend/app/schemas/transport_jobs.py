from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import DeliveryStatus, PickupStatus
from app.schemas.common import BaseReadSchema


class TransportJobCreate(BaseModel):
    route_plan_id: str
    harvest_batch_id: str
    buyer_demand_id: str | None = None
    transporter_id: str
    vehicle_id: str
    agreed_transport_fee: float = Field(gt=0)


class TransportJobUpdate(BaseModel):
    pickup_status: PickupStatus | None = None
    delivery_status: DeliveryStatus | None = None


class TransportJobRead(BaseReadSchema):
    route_plan_id: UUID
    harvest_batch_id: UUID
    buyer_demand_id: UUID | None
    transporter_id: UUID
    vehicle_id: UUID
    pickup_status: PickupStatus
    delivery_status: DeliveryStatus
    agreed_transport_fee: float
