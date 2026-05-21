from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.schemas.notifications import NotificationSendRequest


class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def create_notification(self, *, user_id, channel: str, subject: str, message: str, provider: str, status: str):
        notification = Notification(
            user_id=user_id,
            channel=channel,
            subject=subject,
            message=message,
            provider=provider,
            status=status,
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def send(self, payload: NotificationSendRequest):
        provider = "INTERNAL"
        status_text = "QUEUED"
        return self.create_notification(
            user_id=payload.user_id,
            channel=payload.channel,
            subject=payload.subject,
            message=payload.message,
            provider=provider,
            status=status_text,
        )

    def list(self, page: int, per_page: int):
        rows = self.db.scalars(select(Notification).offset((page - 1) * per_page).limit(per_page)).all()
        total = self.db.query(Notification).count()
        return rows, total

    def get(self, notification_id: UUID):
        notification = self.db.get(Notification, notification_id)
        if not notification:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        return notification

    def mark_read(self, notification_id: UUID):
        notification = self.get(notification_id)
        notification.status = "READ"
        self.db.commit()
        self.db.refresh(notification)
        return notification
