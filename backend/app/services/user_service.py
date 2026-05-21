from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.users import UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def list_users(self, page: int, per_page: int):
        return self.repo.list(page, per_page)

    def get_user(self, user_id: UUID):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def update_user(self, user_id: UUID, payload: UserUpdate):
        user = self.get_user(user_id)
        data = payload.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def activate(self, user_id: UUID, active: bool):
        user = self.get_user(user_id)
        user.is_active = active
        self.db.commit()
        self.db.refresh(user)
        return user
