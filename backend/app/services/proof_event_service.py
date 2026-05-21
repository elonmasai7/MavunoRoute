from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.proof_event import ProofEvent
from app.schemas.proof_events import ProofEventCreate


class ProofEventService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: ProofEventCreate, recorded_by_user_id: UUID):
        event = ProofEvent(**payload.model_dump(), recorded_by_user_id=recorded_by_user_id)
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def list(self, page: int, per_page: int):
        rows = self.db.scalars(select(ProofEvent).offset((page - 1) * per_page).limit(per_page)).all()
        total = self.db.query(ProofEvent).count()
        return rows, total

    def get(self, event_id: UUID):
        event = self.db.get(ProofEvent, event_id)
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proof event not found")
        return event

    def verify_qr(self, qr_code: str):
        event = self.db.query(ProofEvent).filter(ProofEvent.qr_code == qr_code).first()
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="QR proof not found")
        return event
