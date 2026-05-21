from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.buyer_demand import BuyerDemand
from app.repositories.buyer_repository import BuyerRepository
from app.schemas.buyer_demands import BuyerDemandCreate, BuyerDemandUpdate


class BuyerDemandService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = BuyerRepository(db)

    def create(self, payload: BuyerDemandCreate):
        demand = BuyerDemand(**payload.model_dump())
        self.repo.create_demand(demand)
        self.db.commit()
        return demand

    def list(self, page: int, per_page: int):
        return self.repo.list_demands(page, per_page)

    def get(self, demand_id: UUID):
        demand = self.repo.get_demand(demand_id)
        if not demand:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyer demand not found")
        return demand

    def update(self, demand_id: UUID, payload: BuyerDemandUpdate):
        demand = self.get(demand_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(demand, key, value)
        self.db.commit()
        self.db.refresh(demand)
        return demand
