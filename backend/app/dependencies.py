from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.security import decode_token
from app.services.audit_log_service import AuditLogService
from app.utils.permissions import has_permission

bearer_scheme = HTTPBearer(auto_error=False)
PRIVILEGED_ROLES = {"SUPER_ADMIN", "OPS_ADMIN"}


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    try:
        payload = decode_token(credentials.credentials)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")

    user = db.get(User, payload.get("sub"))
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")

    return user


def require_permission(permission: str):
    def checker(current_user: User = Depends(get_current_user)) -> User:
        if not has_permission(current_user.role, permission):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user

    return checker


def get_client_ip(x_forwarded_for: str | None = Header(default=None)) -> str:
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return "unknown"


def enforce_owner_or_privileged(current_user: User, owner_user_id) -> None:
    if current_user.role in PRIVILEGED_ROLES:
        return
    if str(current_user.id) != str(owner_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient ownership permissions")


def audit_action(action: str, entity_type: str):
    def checker(
        request: Request,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        try:
            AuditLogService(db).log(
                user_id=current_user.id,
                action=action,
                entity_type=entity_type,
                entity_id="-",
                ip_address=get_client_ip(request.headers.get("x-forwarded-for")),
                user_agent=request.headers.get("user-agent", "unknown"),
                metadata={"path": request.url.path, "method": request.method},
            )
        except Exception:
            # Auditing must not block primary workflow.
            pass
        return current_user

    return checker
