from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.models.transporter import TransporterProfile
from app.models.transport_job import TransportJob
from app.models.vehicle import Vehicle
from app.schemas.transporters import TransporterCreate, TransporterUpdate


class TransporterService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: TransporterCreate):
        transporter = TransporterProfile(**payload.model_dump())
        self.db.add(transporter)
        self.db.commit()
        self.db.refresh(transporter)
        return transporter

    def list(self, page: int, per_page: int):
        rows = self.db.scalars(select(TransporterProfile).offset((page - 1) * per_page).limit(per_page)).all()
        total = self.db.query(TransporterProfile).count()
        return rows, total

    def get(self, transporter_id: UUID):
        transporter = self.db.get(TransporterProfile, transporter_id)
        if not transporter:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transporter not found")
        return transporter

    def update(self, transporter_id: UUID, payload: TransporterUpdate):
        transporter = self.get(transporter_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(transporter, key, value)
        self.db.commit()
        self.db.refresh(transporter)
        return transporter

    def vehicles(self, transporter_id: UUID):
        self.get(transporter_id)
        return self.db.scalars(select(Vehicle).where(Vehicle.transporter_id == transporter_id)).all()

    def jobs(self, transporter_id: UUID):
        self.get(transporter_id)
        return self.db.scalars(select(TransportJob).where(TransportJob.transporter_id == transporter_id)).all()

    def earnings(self, transporter_id: UUID) -> dict:
        self.get(transporter_id)
        total = float(
            self.db.query(func.coalesce(func.sum(Payment.amount), 0))
            .join(TransportJob, Payment.related_transport_job_id == TransportJob.id, isouter=True)
            .filter(TransportJob.transporter_id == transporter_id)
            .scalar()
            or 0
        )
        return {"transporter_id": str(transporter_id), "total_earnings": total, "currency": "KES"}
