import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import BuyerDemandStatus


class BuyerDemand(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "buyer_demands"

    buyer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("buyer_profiles.id"), nullable=False, index=True)
    crop_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("crops.id"), nullable=False, index=True)
    quantity_kg: Mapped[float] = mapped_column(nullable=False)
    desired_grade: Mapped[str] = mapped_column(String(64), nullable=False)
    max_price_per_kg: Mapped[float] = mapped_column(nullable=False)
    required_delivery_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    delivery_latitude: Mapped[float] = mapped_column(nullable=False)
    delivery_longitude: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[BuyerDemandStatus] = mapped_column(Enum(BuyerDemandStatus), nullable=False, default=BuyerDemandStatus.OPEN)
