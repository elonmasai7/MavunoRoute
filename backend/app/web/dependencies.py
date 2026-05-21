from uuid import UUID

from fastapi import HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.security import decode_token


class WebUser:
    def __init__(self, user: User | None = None):
        self._user = user

    @property
    def is_authenticated(self) -> bool:
        return self._user is not None

    @property
    def id(self) -> UUID | None:
        return self._user.id if self._user else None

    @property
    def full_name(self) -> str | None:
        return self._user.full_name if self._user else None

    @property
    def email(self) -> str | None:
        return self._user.email if self._user else None

    @property
    def phone_number(self) -> str | None:
        return self._user.phone_number if self._user else None

    @property
    def role(self) -> str | None:
        return self._user.role if self._user else None

    @property
    def is_active(self) -> bool:
        return self._user.is_active if self._user else False

    def __bool__(self):
        return self.is_authenticated


def get_web_user(request: Request) -> WebUser:
    token = request.cookies.get("mavuno_access_token")
    if not token:
        return WebUser()
    try:
        payload = decode_token(token)
    except ValueError:
        return WebUser()
    if payload.get("type") != "access":
        return WebUser()
    db: Session = next(get_db())
    try:
        user = db.get(User, UUID(payload.get("sub")))
        if user is None or not user.is_active:
            return WebUser()
        return WebUser(user)
    finally:
        db.close()


def require_web_auth(request: Request) -> WebUser:
    user = get_web_user(request)
    if not user.is_authenticated:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, detail="Authentication required")
    return user


def require_web_role(*roles: str):
    def checker(request: Request) -> WebUser:
        user = get_web_user(request)
        if not user.is_authenticated:
            raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, detail="Authentication required")
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user
    return checker
