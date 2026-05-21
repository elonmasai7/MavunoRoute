from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.payment import MpesaTransaction, Payment


class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_payment(self, payment: Payment) -> Payment:
        self.db.add(payment)
        self.db.flush()
        self.db.refresh(payment)
        return payment

    def get_payment(self, payment_id: UUID) -> Payment | None:
        return self.db.get(Payment, payment_id)

    def list_payments(self, page: int, per_page: int) -> tuple[list[Payment], int]:
        stmt = select(Payment).offset((page - 1) * per_page).limit(per_page)
        rows = self.db.scalars(stmt).all()
        total = self.db.query(Payment).count()
        return rows, total

    def upsert_mpesa_transaction(self, txn: MpesaTransaction) -> MpesaTransaction:
        self.db.add(txn)
        self.db.flush()
        self.db.refresh(txn)
        return txn
