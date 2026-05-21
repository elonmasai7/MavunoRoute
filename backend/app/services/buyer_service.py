from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.buyer import BuyerProfile
from app.schemas.buyers import BuyerCreate


class BuyerService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: BuyerCreate):
        buyer = BuyerProfile(**payload.model_dump())
        self.db.add(buyer)
        self.db.commit()
        self.db.refresh(buyer)
        return buyer

    def list(self, page: int, per_page: int):
        rows = self.db.scalars(select(BuyerProfile).offset((page - 1) * per_page).limit(per_page)).all()
        total = self.db.query(BuyerProfile).count()
        return rows, total

    def get(self, buyer_id: UUID):
        buyer = self.db.get(BuyerProfile, buyer_id)
        if not buyer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyer not found")
        return buyer

    def update(self, buyer_id: UUID, payload: dict):
        buyer = self.get(buyer_id)
        for key, value in payload.items():
            setattr(buyer, key, value)
        self.db.commit()
        self.db.refresh(buyer)
        return buyer
