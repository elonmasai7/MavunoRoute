from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_permission
from app.schemas.users import UserRead, UserUpdate
from app.services.user_service import UserService
from app.utils.pagination import build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
def list_users(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(require_permission("users:read")),
):
    rows, total = UserService(db).list_users(page, per_page)
    data = [UserRead.model_validate(item).model_dump(mode="json") for item in rows]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/{user_id}")
def get_user(user_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("users:read"))):
    user = UserService(db).get_user(user_id)
    return success_response("Record retrieved successfully", UserRead.model_validate(user).model_dump(mode="json"))


@router.patch("/{user_id}")
def update_user(user_id: UUID, payload: UserUpdate, db: Session = Depends(get_db), _=Depends(require_permission("users:write"))):
    user = UserService(db).update_user(user_id, payload)
    return success_response("Record updated successfully", UserRead.model_validate(user).model_dump(mode="json"))


@router.patch("/{user_id}/activate")
def activate_user(user_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("users:write"))):
    user = UserService(db).activate(user_id, True)
    return success_response("User activated successfully", UserRead.model_validate(user).model_dump(mode="json"))


@router.patch("/{user_id}/deactivate")
def deactivate_user(user_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("users:write"))):
    user = UserService(db).activate(user_id, False)
    return success_response("User deactivated successfully", UserRead.model_validate(user).model_dump(mode="json"))
