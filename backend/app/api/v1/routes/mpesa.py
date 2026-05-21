from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import audit_action, require_permission
from app.models.payment import MpesaTransaction
from app.services.mpesa_service import MpesaService
from app.services.payment_service import PaymentService
from app.utils.response import success_response

router = APIRouter(prefix="/mpesa", tags=["M-Pesa"])


@router.post("/stk-push")
async def stk_push(
    payload: dict,
    db: Session = Depends(get_db),
    _=Depends(require_permission("payments:write")),
    __=Depends(audit_action("MPESA_STK_PUSH", "PAYMENT")),
):
    payment = PaymentService(db).get(payload["payment_id"])
    data = await MpesaService(db).stk_push(payment, payload["phone_number"])
    return success_response("Operation completed successfully", data)


@router.post("/callback")
def callback(
    payload: dict,
    db: Session = Depends(get_db),
    x_callback_signature: str | None = Header(default=None),
):
    data = MpesaService(db).callback(payload, signature=x_callback_signature)
    return success_response("Operation completed successfully", data)


@router.post("/query")
def query_transaction(payload: dict, db: Session = Depends(get_db), _=Depends(require_permission("payments:read"))):
    txn = db.query(MpesaTransaction).filter(MpesaTransaction.checkout_request_id == payload["checkout_request_id"]).first()
    if not txn:
        return success_response("Record not found", {})
    return success_response(
        "Record retrieved successfully",
        {
            "checkout_request_id": txn.checkout_request_id,
            "result_code": txn.result_code,
            "result_description": txn.result_description,
        },
    )


@router.get("/transactions")
def list_transactions(db: Session = Depends(get_db), _=Depends(require_permission("payments:read"))):
    rows = db.query(MpesaTransaction).all()
    return success_response(
        "Records retrieved successfully",
        [{"id": str(item.id), "checkout_request_id": item.checkout_request_id, "result_code": item.result_code} for item in rows],
    )


@router.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: str, db: Session = Depends(get_db), _=Depends(require_permission("payments:read"))):
    item = db.get(MpesaTransaction, transaction_id)
    if not item:
        return success_response("Record not found", {})
    return success_response(
        "Record retrieved successfully",
        {
            "id": str(item.id),
            "checkout_request_id": item.checkout_request_id,
            "result_code": item.result_code,
            "result_description": item.result_description,
        },
    )
