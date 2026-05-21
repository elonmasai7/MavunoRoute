from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email))

    def get_by_id(self, user_id: UUID) -> User | None:
        return self.db.get(User, user_id)

    def list(self, page: int, per_page: int) -> tuple[list[User], int]:
        stmt = select(User).offset((page - 1) * per_page).limit(per_page)
        rows = self.db.scalars(stmt).all()
        total = self.db.query(User).count()
        return rows, total
