from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import audit_action, require_permission
from app.schemas.cold_hubs import CapacityUpdate, ColdHubCreate, ColdHubRead, ColdHubUpdate
from app.services.cold_hub_service import ColdHubService
from app.utils.pagination import build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/cold-hubs", tags=["Cold Hubs"])


@router.post("")
def create_cold_hub(
    payload: ColdHubCreate,
    db: Session = Depends(get_db),
    _=Depends(require_permission("cold_hubs:write")),
    __=Depends(audit_action("COLD_HUB_CREATE", "COLD_HUB")),
):
    hub = ColdHubService(db).create(payload)
    return success_response("Operation completed successfully", ColdHubRead.model_validate(hub).model_dump(mode="json"))


@router.get("")
def list_cold_hubs(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(require_permission("cold_hubs:read")),
):
    rows, total = ColdHubService(db).list(page, per_page)
    data = [ColdHubRead.model_validate(item).model_dump(mode="json") for item in rows]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/nearby")
def nearby_hubs(
    latitude: float,
    longitude: float,
    radius_km: float = Query(default=30, gt=0),
    db: Session = Depends(get_db),
    _=Depends(require_permission("cold_hubs:read")),
):
    hubs = ColdHubService(db).nearby(latitude, longitude, radius_km)
    return success_response(
        "Records retrieved successfully",
        [
            {"hub": ColdHubRead.model_validate(item[0]).model_dump(mode="json"), "distance_km": round(item[1], 2)}
            for item in hubs
        ],
    )


@router.get("/{hub_id}")
def get_cold_hub(hub_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("cold_hubs:read"))):
    hub = ColdHubService(db).get(hub_id)
    return success_response("Record retrieved successfully", ColdHubRead.model_validate(hub).model_dump(mode="json"))


@router.patch("/{hub_id}")
def update_cold_hub(
    hub_id: UUID,
    payload: ColdHubUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_permission("cold_hubs:write")),
    __=Depends(audit_action("COLD_HUB_UPDATE", "COLD_HUB")),
):
    hub = ColdHubService(db).update(hub_id, payload)
    return success_response("Record updated successfully", ColdHubRead.model_validate(hub).model_dump(mode="json"))


@router.patch("/{hub_id}/capacity")
def update_capacity(
    hub_id: UUID,
    payload: CapacityUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_permission("cold_hubs:write")),
    __=Depends(audit_action("COLD_HUB_CAPACITY_UPDATE", "COLD_HUB")),
):
    hub = ColdHubService(db).update_capacity(hub_id, payload.available_capacity_kg)
    return success_response("Operation completed successfully", ColdHubRead.model_validate(hub).model_dump(mode="json"))


@router.post("/{hub_id}/check-in")
def check_in(
    hub_id: UUID,
    payload: dict,
    db: Session = Depends(get_db),
    _=Depends(require_permission("cold_hubs:write")),
    __=Depends(audit_action("COLD_HUB_CHECK_IN", "COLD_HUB")),
):
    hub = ColdHubService(db).check_in(hub_id, payload["quantity_kg"])
    return success_response("Operation completed successfully", ColdHubRead.model_validate(hub).model_dump(mode="json"))


@router.post("/{hub_id}/check-out")
def check_out(
    hub_id: UUID,
    payload: dict,
    db: Session = Depends(get_db),
    _=Depends(require_permission("cold_hubs:write")),
    __=Depends(audit_action("COLD_HUB_CHECK_OUT", "COLD_HUB")),
):
    hub = ColdHubService(db).check_out(hub_id, payload["quantity_kg"])
    return success_response("Operation completed successfully", ColdHubRead.model_validate(hub).model_dump(mode="json"))
