from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import audit_action, require_permission
from app.models.farmer import FarmerProfile
from app.models.harvest_batch import HarvestBatch
from app.schemas.cooperatives import CooperativeCreate, CooperativeRead, CooperativeUpdate
from app.schemas.farmers import FarmerRead
from app.services.cooperative_service import CooperativeService
from app.utils.pagination import build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/cooperatives", tags=["Cooperatives"])


@router.post("")
def create_cooperative(
    payload: CooperativeCreate,
    db: Session = Depends(get_db),
    _=Depends(require_permission("cooperatives:write")),
    __=Depends(audit_action("COOPERATIVE_CREATE", "COOPERATIVE")),
):
    model = CooperativeService(db).create(payload)
    return success_response("Operation completed successfully", CooperativeRead.model_validate(model).model_dump(mode="json"))


@router.get("")
def list_cooperatives(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(require_permission("cooperatives:read")),
):
    rows, total = CooperativeService(db).list(page, per_page)
    data = [CooperativeRead.model_validate(item).model_dump(mode="json") for item in rows]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/{cooperative_id}")
def get_cooperative(cooperative_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("cooperatives:read"))):
    model = CooperativeService(db).get(cooperative_id)
    return success_response("Record retrieved successfully", CooperativeRead.model_validate(model).model_dump(mode="json"))


@router.patch("/{cooperative_id}")
def update_cooperative(
    cooperative_id: UUID,
    payload: CooperativeUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_permission("cooperatives:write")),
    __=Depends(audit_action("COOPERATIVE_UPDATE", "COOPERATIVE")),
):
    model = CooperativeService(db).update(cooperative_id, payload)
    return success_response("Record updated successfully", CooperativeRead.model_validate(model).model_dump(mode="json"))


@router.post("/{cooperative_id}/farmers")
def add_farmer_to_cooperative(
    cooperative_id: UUID,
    payload: dict,
    db: Session = Depends(get_db),
    _=Depends(require_permission("cooperatives:write")),
    __=Depends(audit_action("COOPERATIVE_ADD_FARMER", "COOPERATIVE")),
):
    farmer = CooperativeService(db).add_farmer(cooperative_id, UUID(payload["farmer_id"]))
    return success_response("Operation completed successfully", FarmerRead.model_validate(farmer).model_dump(mode="json"))


@router.get("/{cooperative_id}/farmers")
def list_cooperative_farmers(
    cooperative_id: UUID,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(require_permission("cooperatives:read")),
):
    rows, total = CooperativeService(db).list_farmers(cooperative_id, page, per_page)
    data = [FarmerRead.model_validate(item).model_dump(mode="json") for item in rows]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/{cooperative_id}/harvests")
def cooperative_harvests(cooperative_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("cooperatives:read"))):
    CooperativeService(db).get(cooperative_id)
    rows = db.query(HarvestBatch).join(FarmerProfile, HarvestBatch.farmer_id == FarmerProfile.id).filter(FarmerProfile.cooperative_id == cooperative_id).all()
    return success_response(
        "Records retrieved successfully",
        [{"id": str(item.id), "crop_id": str(item.crop_id), "quantity_kg": item.quantity_kg, "status": item.status} for item in rows],
    )


@router.get("/{cooperative_id}/reports")
def cooperative_reports(cooperative_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("reports:read"))):
    rows, _ = CooperativeService(db).list_farmers(cooperative_id, 1, 100000)
    return success_response(
        "Records retrieved successfully",
        {"cooperative_id": str(cooperative_id), "total_farmers": len(rows)},
    )
