from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import audit_action, require_permission
from app.schemas.notifications import NotificationRead, NotificationSendRequest
from app.services.notification_service import NotificationService
from app.utils.pagination import build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.post("/send")
def send_notification(
    payload: NotificationSendRequest,
    db: Session = Depends(get_db),
    _=Depends(require_permission("notifications:write")),
    __=Depends(audit_action("NOTIFICATION_SEND", "NOTIFICATION")),
):
    notification = NotificationService(db).send(payload)
    return success_response(
        "Operation completed successfully",
        NotificationRead(
            id=str(notification.id),
            user_id=str(notification.user_id),
            channel=notification.channel,
            subject=notification.subject,
            message=notification.message,
            provider=notification.provider,
            status=notification.status,
            provider_reference=notification.provider_reference,
            created_at=notification.created_at,
        ).model_dump(mode="json"),
    )


@router.get("")
def list_notifications(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(require_permission("notifications:read")),
):
    rows, total = NotificationService(db).list(page, per_page)
    data = [
        NotificationRead(
            id=str(item.id),
            user_id=str(item.user_id),
            channel=item.channel,
            subject=item.subject,
            message=item.message,
            provider=item.provider,
            status=item.status,
            provider_reference=item.provider_reference,
            created_at=item.created_at,
        ).model_dump(mode="json")
        for item in rows
    ]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/{notification_id}")
def get_notification(notification_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("notifications:read"))):
    item = NotificationService(db).get(notification_id)
    data = NotificationRead(
        id=str(item.id),
        user_id=str(item.user_id),
        channel=item.channel,
        subject=item.subject,
        message=item.message,
        provider=item.provider,
        status=item.status,
        provider_reference=item.provider_reference,
        created_at=item.created_at,
    ).model_dump(mode="json")
    return success_response("Record retrieved successfully", data)


@router.patch("/{notification_id}/read")
def mark_read(
    notification_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_permission("notifications:read")),
    __=Depends(audit_action("NOTIFICATION_READ", "NOTIFICATION")),
):
    item = NotificationService(db).mark_read(notification_id)
    return success_response("Operation completed successfully", {"id": str(item.id), "status": item.status})
