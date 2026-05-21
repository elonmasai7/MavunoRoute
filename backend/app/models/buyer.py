import uuid

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import VerificationStatus


class BuyerProfile(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "buyer_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    business_name: Mapped[str] = mapped_column(String(255), nullable=False)
    business_type: Mapped[str] = mapped_column(String(128), nullable=False)
    kra_pin: Mapped[str | None] = mapped_column(String(32), nullable=True)
    county: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    delivery_address: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    verification_status: Mapped[VerificationStatus] = mapped_column(
        Enum(VerificationStatus), nullable=False, default=VerificationStatus.PENDING
    )
