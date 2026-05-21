from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.farmer import FarmerProfile


class FarmerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, model: FarmerProfile) -> FarmerProfile:
        self.db.add(model)
        self.db.flush()
        self.db.refresh(model)
        return model

    def get(self, farmer_id: UUID) -> FarmerProfile | None:
        return self.db.get(FarmerProfile, farmer_id)

    def list(self, page: int, per_page: int) -> tuple[list[FarmerProfile], int]:
        stmt = select(FarmerProfile).offset((page - 1) * per_page).limit(per_page)
        rows = self.db.scalars(stmt).all()
        total = self.db.query(FarmerProfile).count()
        return rows, total
