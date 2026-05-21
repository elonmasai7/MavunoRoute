from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Cooperative(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "cooperatives"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    registration_number: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    county: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    contact_person: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(32), nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
