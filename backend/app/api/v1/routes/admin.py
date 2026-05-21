from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_permission
from app.models.audit_log import AuditLog
from app.models.integration_log import ApiIntegrationLog
from app.services.report_service import ReportService
from app.utils.pagination import build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/overview")
def overview(db: Session = Depends(get_db), _=Depends(require_permission("admin:read"))):
    return success_response("Records retrieved successfully", ReportService(db).dashboard_metrics())


@router.get("/audit-logs")
def audit_logs(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(require_permission("admin:read")),
):
    rows = db.scalars(select(AuditLog).offset((page - 1) * per_page).limit(per_page)).all()
    total = db.query(AuditLog).count()
    data = [
        {
            "id": str(item.id),
            "user_id": str(item.user_id) if item.user_id else None,
            "action": item.action,
            "entity_type": item.entity_type,
            "entity_id": item.entity_id,
            "created_at": item.created_at,
        }
        for item in rows
    ]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/integration-logs")
def integration_logs(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(require_permission("admin:read")),
):
    rows = db.scalars(select(ApiIntegrationLog).offset((page - 1) * per_page).limit(per_page)).all()
    total = db.query(ApiIntegrationLog).count()
    data = [
        {
            "id": str(item.id),
            "provider": item.provider,
            "request_type": item.request_type,
            "status": item.status,
            "response_code": item.response_code,
            "created_at": item.created_at,
        }
        for item in rows
    ]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/system-health")
def system_health(db: Session = Depends(get_db), _=Depends(require_permission("admin:read"))):
    return success_response(
        "Records retrieved successfully",
        {
            "api": "ok",
            "database": "ok",
            "pending_integrations": db.query(ApiIntegrationLog).filter(ApiIntegrationLog.status != "SUCCESS").count(),
        },
    )


@router.patch("/settings")
def update_settings(payload: dict, _=Depends(require_permission("admin:write"))):
    return success_response("Operation completed successfully", {"applied_settings": payload})
