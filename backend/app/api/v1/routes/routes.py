from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import audit_action, require_permission
from app.schemas.routes import RoutePlanCreate, RouteRead
from app.services.route_optimization_service import RouteOptimizationService
from app.utils.pagination import build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/routes", tags=["Route Planning"])


@router.post("/plan")
async def plan_route(
    payload: RoutePlanCreate,
    db: Session = Depends(get_db),
    _=Depends(require_permission("routes:write")),
    __=Depends(audit_action("ROUTE_PLAN", "ROUTE")),
):
    data = await RouteOptimizationService(db).plan_route(payload)
    return success_response("Operation completed successfully", data)


@router.get("")
def list_routes(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(require_permission("routes:read")),
):
    rows, total = RouteOptimizationService(db).repo.list_routes(page, per_page)
    data = [RouteRead.model_validate(item).model_dump(mode="json") for item in rows]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/{route_id}")
def get_route(route_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("routes:read"))):
    route = RouteOptimizationService(db).repo.get_route(route_id)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return success_response("Record retrieved successfully", RouteRead.model_validate(route).model_dump(mode="json"))


@router.patch("/{route_id}")
def update_route(
    route_id: UUID,
    payload: dict,
    db: Session = Depends(get_db),
    _=Depends(require_permission("routes:write")),
    __=Depends(audit_action("ROUTE_UPDATE", "ROUTE")),
):
    route = RouteOptimizationService(db).update_route(route_id, payload)
    return success_response("Record updated successfully", RouteRead.model_validate(route).model_dump(mode="json"))


@router.patch("/{route_id}/assign-vehicle")
def assign_vehicle(
    route_id: UUID,
    payload: dict,
    db: Session = Depends(get_db),
    _=Depends(require_permission("routes:write")),
    __=Depends(audit_action("ROUTE_ASSIGN_VEHICLE", "ROUTE")),
):
    route = RouteOptimizationService(db).assign_vehicle(route_id, payload["vehicle_id"])
    return success_response("Operation completed successfully", RouteRead.model_validate(route).model_dump(mode="json"))


@router.patch("/{route_id}/start")
def start_route(
    route_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_permission("routes:write")),
    __=Depends(audit_action("ROUTE_START", "ROUTE")),
):
    route = RouteOptimizationService(db).start_route(route_id)
    return success_response("Operation completed successfully", RouteRead.model_validate(route).model_dump(mode="json"))


@router.patch("/{route_id}/complete")
def complete_route(
    route_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_permission("routes:write")),
    __=Depends(audit_action("ROUTE_COMPLETE", "ROUTE")),
):
    route = RouteOptimizationService(db).complete_route(route_id)
    return success_response("Operation completed successfully", RouteRead.model_validate(route).model_dump(mode="json"))


@router.get("/{route_id}/stops")
def route_stops(route_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("routes:read"))):
    stops = RouteOptimizationService(db).route_stops(route_id)
    return success_response(
        "Records retrieved successfully",
        [
            {
                "id": str(stop.id),
                "stop_type": stop.stop_type,
                "sequence_number": stop.sequence_number,
                "status": stop.status,
                "latitude": stop.latitude,
                "longitude": stop.longitude,
            }
            for stop in stops
        ],
    )


@router.post("/{route_id}/recalculate")
async def recalculate_route(
    route_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_permission("routes:write")),
    __=Depends(audit_action("ROUTE_RECALCULATE", "ROUTE")),
):
    data = await RouteOptimizationService(db).route_map(route_id)
    return success_response("Operation completed successfully", data)


@router.get("/{route_id}/map")
async def route_map(route_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("routes:read"))):
    data = await RouteOptimizationService(db).route_map(route_id)
    return success_response("Record retrieved successfully", data)
