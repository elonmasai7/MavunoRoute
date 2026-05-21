from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import audit_action, require_permission
from app.models.payment import Payment
from app.models.enums import PaymentStatus
from app.schemas.payments import PaymentInitiate, PaymentRead
from app.services.payment_service import PaymentService
from app.utils.pagination import build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/initiate")
def initiate_payment(
    payload: PaymentInitiate,
    db: Session = Depends(get_db),
    _=Depends(require_permission("payments:write")),
    __=Depends(audit_action("PAYMENT_INITIATE", "PAYMENT")),
):
    payment = PaymentService(db).initiate(payload)
    return success_response("Operation completed successfully", PaymentRead.model_validate(payment).model_dump(mode="json"))


@router.get("")
def list_payments(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(require_permission("payments:read")),
):
    rows, total = PaymentService(db).list(page, per_page)
    data = [PaymentRead.model_validate(item).model_dump(mode="json") for item in rows]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/{payment_id}")
def get_payment(payment_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("payments:read"))):
    payment = PaymentService(db).get(payment_id)
    return success_response("Record retrieved successfully", PaymentRead.model_validate(payment).model_dump(mode="json"))


@router.post("/{payment_id}/cancel")
def cancel_payment(
    payment_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_permission("payments:write")),
    __=Depends(audit_action("PAYMENT_CANCEL", "PAYMENT")),
):
    payment = PaymentService(db).mark_cancelled(payment_id)
    return success_response("Operation completed successfully", PaymentRead.model_validate(payment).model_dump(mode="json"))


@router.post("/{payment_id}/confirm")
def confirm_payment(
    payment_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_permission("payments:write")),
    __=Depends(audit_action("PAYMENT_CONFIRM", "PAYMENT")),
):
    payment = PaymentService(db).get(payment_id)
    payment.status = PaymentStatus.PAID
    db.commit()
    db.refresh(payment)
    return success_response("Operation completed successfully", PaymentRead.model_validate(payment).model_dump(mode="json"))


@router.get("/user/{user_id}")
def user_payments(user_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("payments:read"))):
    rows = db.query(Payment).filter((Payment.payer_user_id == user_id) | (Payment.payee_user_id == user_id)).all()
    data = [PaymentRead.model_validate(item).model_dump(mode="json") for item in rows]
    return success_response("Records retrieved successfully", data)


@router.get("/reconciliation")
def reconciliation(db: Session = Depends(get_db), _=Depends(require_permission("payments:read"))):
    pending = db.query(Payment).filter(Payment.status == PaymentStatus.PROCESSING).count()
    total = float(db.query(func.coalesce(func.sum(Payment.amount), 0)).scalar() or 0)
    return success_response("Records retrieved successfully", {"pending_reconciliation": pending, "total_value": total})
