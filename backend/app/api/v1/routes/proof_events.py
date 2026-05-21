from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import audit_action, get_current_user, require_permission
from app.schemas.proof_events import ProofEventCreate
from app.services.proof_event_service import ProofEventService
from app.utils.pagination import build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/proof-events", tags=["Proof Events"])


@router.post("")
def create_proof_event(
    payload: ProofEventCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    _=Depends(require_permission("proofs:write")),
    __=Depends(audit_action("PROOF_CREATE", "PROOF_EVENT")),
):
    event = ProofEventService(db).create(payload, recorded_by_user_id=current_user.id)
    return success_response("Operation completed successfully", {"id": str(event.id), "qr_code": event.qr_code})


@router.get("")
def list_proof_events(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(require_permission("proofs:read")),
):
    rows, total = ProofEventService(db).list(page, per_page)
    data = [{"id": str(item.id), "event_type": item.event_type, "qr_code": item.qr_code} for item in rows]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/{event_id}")
def get_proof_event(event_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("proofs:read"))):
    event = ProofEventService(db).get(event_id)
    return success_response(
        "Record retrieved successfully",
        {"id": str(event.id), "event_type": event.event_type, "qr_code": event.qr_code},
    )


@router.get("/verify/{qr_code}")
def verify_proof_event(qr_code: str, db: Session = Depends(get_db), _=Depends(require_permission("proofs:read"))):
    event = ProofEventService(db).verify_qr(qr_code)
    return success_response("Proof event verified successfully", {"id": str(event.id), "event_type": event.event_type})


@router.post("/pickup")
def pickup_proof(
    payload: ProofEventCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    _=Depends(require_permission("proofs:write")),
    __=Depends(audit_action("PROOF_PICKUP", "PROOF_EVENT")),
):
    event = ProofEventService(db).create(payload.model_copy(update={"event_type": "PICKUP"}), recorded_by_user_id=current_user.id)
    return success_response("Operation completed successfully", {"id": str(event.id), "qr_code": event.qr_code})


@router.post("/delivery")
def delivery_proof(
    payload: ProofEventCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    _=Depends(require_permission("proofs:write")),
    __=Depends(audit_action("PROOF_DELIVERY", "PROOF_EVENT")),
):
    event = ProofEventService(db).create(payload.model_copy(update={"event_type": "DELIVERY"}), recorded_by_user_id=current_user.id)
    return success_response("Operation completed successfully", {"id": str(event.id), "qr_code": event.qr_code})
