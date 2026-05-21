from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.models.enums import PaymentStatus
from app.repositories.payment_repository import PaymentRepository
from app.schemas.payments import PaymentInitiate


class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PaymentRepository(db)

    def initiate(self, payload: PaymentInitiate):
        payment = Payment(**payload.model_dump(), status=PaymentStatus.PENDING)
        self.repo.create_payment(payment)
        self.db.commit()
        return payment

    def get(self, payment_id: UUID):
        payment = self.repo.get_payment(payment_id)
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
        return payment

    def list(self, page: int, per_page: int):
        return self.repo.list_payments(page, per_page)

    def mark_cancelled(self, payment_id: UUID):
        payment = self.get(payment_id)
        payment.status = PaymentStatus.CANCELLED
        self.db.commit()
        return payment
