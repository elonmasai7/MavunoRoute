from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditLogService:
    def __init__(self, db: Session):
        self.db = db

    def log(self, *, user_id, action: str, entity_type: str, entity_id: str, ip_address: str, user_agent: str, metadata: dict):
        self.db.add(
            AuditLog(
                user_id=user_id,
                action=action,
                entity_type=entity_type,
                entity_id=entity_id,
                ip_address=ip_address,
                user_agent=user_agent,
                metadata_json=metadata,
            )
        )
        self.db.flush()
