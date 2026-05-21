from datetime import UTC, datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import RefreshToken, User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest
from app.security import create_access_token, create_refresh_token, decode_token, hash_password, verify_password


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, payload: RegisterRequest) -> dict:
        existing = self.user_repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

        user = User(
            full_name=payload.full_name,
            email=payload.email,
            phone_number=payload.phone_number,
            password_hash=hash_password(payload.password),
            role=payload.role,
            is_active=True,
            is_verified=False,
        )
        self.user_repo.create(user)
        self.db.commit()

        return {"user_id": str(user.id), "email": user.email, "role": user.role}

    def login(self, payload: LoginRequest) -> dict:
        user = self.user_repo.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account inactive")

        access_token, access_expires = create_access_token(str(user.id), user.role)
        refresh_token, refresh_expires, refresh_jti = create_refresh_token(str(user.id), user.role)
        self.db.add(
            RefreshToken(
                user_id=user.id,
                jti=refresh_jti,
                is_revoked=False,
                expires_at=refresh_expires,
                created_at=datetime.now(UTC),
            )
        )
        self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_at": access_expires.isoformat(),
            "role": user.role,
        }

    def refresh(self, payload: RefreshRequest) -> dict:
        token_payload = decode_token(payload.refresh_token)
        if token_payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        jti = token_payload.get("jti")
        db_token = self.db.query(RefreshToken).filter(RefreshToken.jti == jti).first()
        if not db_token or db_token.is_revoked:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked")

        user = self.user_repo.get_by_id(UUID(token_payload["sub"]))
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User unavailable")

        access_token, access_expires = create_access_token(str(user.id), user.role)
        return {"access_token": access_token, "token_type": "bearer", "expires_at": access_expires.isoformat()}

    def logout(self, refresh_token: str) -> None:
        token_payload = decode_token(refresh_token)
        db_token = self.db.query(RefreshToken).filter(RefreshToken.jti == token_payload.get("jti")).first()
        if db_token:
            db_token.is_revoked = True
            self.db.commit()
