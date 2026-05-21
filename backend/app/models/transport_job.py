import uuid

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import DeliveryStatus, PickupStatus


class TransportJob(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "transport_jobs"

    route_plan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("route_plans.id"), nullable=False, index=True)
    harvest_batch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("harvest_batches.id"), nullable=False, index=True
    )
    buyer_demand_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("buyer_demands.id"), nullable=True)
    transporter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("transporter_profiles.id"), nullable=False, index=True
    )
    vehicle_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=False, index=True)
    pickup_status: Mapped[PickupStatus] = mapped_column(Enum(PickupStatus), nullable=False, default=PickupStatus.PENDING, index=True)
    delivery_status: Mapped[DeliveryStatus] = mapped_column(
        Enum(DeliveryStatus), nullable=False, default=DeliveryStatus.PENDING, index=True
    )
    agreed_transport_fee: Mapped[float] = mapped_column(nullable=False)
