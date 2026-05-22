from uuid import UUID

from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.security import decode_token


def _resolve_db_from_request(request: Request) -> tuple[Session, object]:
    override = request.app.dependency_overrides.get(get_db)
    provider = override or get_db
    generator = provider()
    session = next(generator)
    return session, generator


def _cleanup_db_generator(generator: object) -> None:
    try:
        next(generator)
    except StopIteration:
        pass
    except Exception:
        pass


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
    subject = payload.get("sub")
    if not subject:
        return WebUser()
    try:
        user_id = UUID(str(subject))
    except (TypeError, ValueError):
        return WebUser()

    db, generator = _resolve_db_from_request(request)
    try:
        user = db.get(User, user_id)
        if user is None or not user.is_active:
            return WebUser()
        return WebUser(user)
    finally:
        _cleanup_db_generator(generator)


def require_web_auth(request: Request) -> WebUser:
    user = get_web_user(request)
    if not user.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    return user


def require_web_role(*roles: str):
    def checker(request: Request) -> WebUser:
        user = get_web_user(request)
        if not user.is_authenticated:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user

    return checker
