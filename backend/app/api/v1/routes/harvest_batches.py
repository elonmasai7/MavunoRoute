from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import audit_action, enforce_owner_or_privileged, get_current_user, require_permission
from app.models.farmer import FarmerProfile
from app.models.proof_event import ProofEvent
from app.models.temperature_event import TemperatureEvent
from app.models.transport_job import TransportJob
from app.schemas.harvest_batches import HarvestBatchCreate, HarvestBatchRead, HarvestBatchUpdate
from app.services.harvest_batch_service import HarvestBatchService
from app.utils.pagination import build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/harvest-batches", tags=["Harvest Batches"])


@router.post("")
def create_harvest_batch(
    payload: HarvestBatchCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("harvests:write")),
    __=Depends(audit_action("HARVEST_CREATE", "HARVEST_BATCH")),
):
    if current_user.role == "FARMER":
        farmer = db.get(FarmerProfile, payload.farmer_id)
        if not farmer:
            raise HTTPException(status_code=404, detail="Farmer profile not found")
        enforce_owner_or_privileged(current_user, farmer.user_id)
    batch = HarvestBatchService(db).create(payload)
    return success_response("Operation completed successfully", HarvestBatchRead.model_validate(batch).model_dump(mode="json"))


@router.get("")
def list_harvest_batches(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(require_permission("harvests:read")),
):
    rows, total = HarvestBatchService(db).list(page, per_page)
    data = [HarvestBatchRead.model_validate(item).model_dump(mode="json") for item in rows]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/{batch_id}")
def get_harvest_batch(
    batch_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("harvests:read")),
):
    batch = HarvestBatchService(db).get(batch_id)
    if current_user.role == "FARMER":
        farmer = db.get(FarmerProfile, batch.farmer_id)
        if farmer:
            enforce_owner_or_privileged(current_user, farmer.user_id)
    return success_response("Record retrieved successfully", HarvestBatchRead.model_validate(batch).model_dump(mode="json"))


@router.patch("/{batch_id}")
def update_harvest_batch(
    batch_id: UUID,
    payload: HarvestBatchUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("harvests:write")),
    __=Depends(audit_action("HARVEST_UPDATE", "HARVEST_BATCH")),
):
    existing = HarvestBatchService(db).get(batch_id)
    if current_user.role == "FARMER":
        farmer = db.get(FarmerProfile, existing.farmer_id)
        if farmer:
            enforce_owner_or_privileged(current_user, farmer.user_id)
    batch = HarvestBatchService(db).update(batch_id, payload)
    return success_response("Record updated successfully", HarvestBatchRead.model_validate(batch).model_dump(mode="json"))


@router.post("/{batch_id}/calculate-spoilage-risk")
async def calculate_spoilage_risk(
    batch_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_permission("harvests:write")),
):
    data = await HarvestBatchService(db).calculate_spoilage_risk(batch_id)
    return success_response("Operation completed successfully", data)


@router.patch("/{batch_id}/status")
def update_harvest_status(
    batch_id: UUID,
    payload: dict,
    db: Session = Depends(get_db),
    _=Depends(require_permission("harvests:write")),
    __=Depends(audit_action("HARVEST_STATUS_UPDATE", "HARVEST_BATCH")),
):
    batch = HarvestBatchService(db).update(batch_id, HarvestBatchUpdate(status=payload["status"]))
    return success_response("Operation completed successfully", HarvestBatchRead.model_validate(batch).model_dump(mode="json"))


@router.get("/{batch_id}/temperature-events")
def batch_temperature_events(batch_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("temperature:read"))):
    events = db.query(TemperatureEvent).filter(TemperatureEvent.harvest_batch_id == batch_id).all()
    return success_response(
        "Records retrieved successfully",
        [{"id": str(item.id), "temperature_celsius": item.temperature_celsius, "recorded_at": item.recorded_at} for item in events],
    )


@router.get("/{batch_id}/proof-events")
def batch_proof_events(batch_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("proofs:read"))):
    events = db.query(ProofEvent).join(TransportJob, ProofEvent.transport_job_id == TransportJob.id).filter(TransportJob.harvest_batch_id == batch_id).all()
    return success_response(
        "Records retrieved successfully",
        [{"id": str(item.id), "event_type": item.event_type, "qr_code": item.qr_code} for item in events],
    )
