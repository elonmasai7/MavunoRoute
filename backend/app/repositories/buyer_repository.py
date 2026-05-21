from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.buyer import BuyerProfile
from app.models.buyer_demand import BuyerDemand


class BuyerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_buyer(self, model: BuyerProfile) -> BuyerProfile:
        self.db.add(model)
        self.db.flush()
        self.db.refresh(model)
        return model

    def get_buyer(self, buyer_id: UUID) -> BuyerProfile | None:
        return self.db.get(BuyerProfile, buyer_id)

    def create_demand(self, model: BuyerDemand) -> BuyerDemand:
        self.db.add(model)
        self.db.flush()
        self.db.refresh(model)
        return model

    def get_demand(self, demand_id: UUID) -> BuyerDemand | None:
        return self.db.get(BuyerDemand, demand_id)

    def list_demands(self, page: int, per_page: int) -> tuple[list[BuyerDemand], int]:
        stmt = select(BuyerDemand).offset((page - 1) * per_page).limit(per_page)
        rows = self.db.scalars(stmt).all()
        total = self.db.query(BuyerDemand).count()
        return rows, total
