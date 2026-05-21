from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import DeliveryStatus, PickupStatus
from app.models.transport_job import TransportJob
from app.schemas.transport_jobs import TransportJobCreate, TransportJobUpdate


class TransportJobService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: TransportJobCreate):
        job = TransportJob(**payload.model_dump())
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def list(self, page: int, per_page: int):
        rows = self.db.scalars(select(TransportJob).offset((page - 1) * per_page).limit(per_page)).all()
        total = self.db.query(TransportJob).count()
        return rows, total

    def get(self, job_id: UUID):
        job = self.db.get(TransportJob, job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transport job not found")
        return job

    def update(self, job_id: UUID, payload: TransportJobUpdate):
        job = self.get(job_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(job, key, value)
        self.db.commit()
        self.db.refresh(job)
        return job

    def accept(self, job_id: UUID):
        job = self.get(job_id)
        job.pickup_status = PickupStatus.ACCEPTED
        self.db.commit()
        return job

    def mark_pickup(self, job_id: UUID):
        job = self.get(job_id)
        job.pickup_status = PickupStatus.PICKED
        job.delivery_status = DeliveryStatus.IN_TRANSIT
        self.db.commit()
        return job

    def mark_delivery(self, job_id: UUID):
        job = self.get(job_id)
        job.delivery_status = DeliveryStatus.DELIVERED
        self.db.commit()
        return job

    def reject(self, job_id: UUID):
        job = self.get(job_id)
        job.pickup_status = PickupStatus.REJECTED
        self.db.commit()
        return job

    def cancel(self, job_id: UUID):
        job = self.get(job_id)
        job.pickup_status = PickupStatus.CANCELLED
        job.delivery_status = DeliveryStatus.CANCELLED
        self.db.commit()
        return job
