from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cooperative import Cooperative
from app.models.farmer import FarmerProfile
from app.schemas.cooperatives import CooperativeCreate, CooperativeUpdate


class CooperativeService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: CooperativeCreate):
        cooperative = Cooperative(**payload.model_dump())
        self.db.add(cooperative)
        self.db.commit()
        self.db.refresh(cooperative)
        return cooperative

    def list(self, page: int, per_page: int):
        rows = self.db.scalars(select(Cooperative).offset((page - 1) * per_page).limit(per_page)).all()
        total = self.db.query(Cooperative).count()
        return rows, total

    def get(self, cooperative_id: UUID):
        cooperative = self.db.get(Cooperative, cooperative_id)
        if not cooperative:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cooperative not found")
        return cooperative

    def update(self, cooperative_id: UUID, payload: CooperativeUpdate):
        cooperative = self.get(cooperative_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(cooperative, key, value)
        self.db.commit()
        self.db.refresh(cooperative)
        return cooperative

    def add_farmer(self, cooperative_id: UUID, farmer_id: UUID):
        self.get(cooperative_id)
        farmer = self.db.get(FarmerProfile, farmer_id)
        if not farmer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farmer not found")
        farmer.cooperative_id = cooperative_id
        self.db.commit()
        return farmer

    def list_farmers(self, cooperative_id: UUID, page: int, per_page: int):
        self.get(cooperative_id)
        rows = self.db.scalars(
            select(FarmerProfile).where(FarmerProfile.cooperative_id == cooperative_id).offset((page - 1) * per_page).limit(per_page)
        ).all()
        total = self.db.query(FarmerProfile).filter(FarmerProfile.cooperative_id == cooperative_id).count()
        return rows, total
