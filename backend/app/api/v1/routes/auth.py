from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest
from app.services.auth_service import AuthService
from app.utils.response import success_response

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    data = AuthService(db).register(payload)
    return success_response("Registration completed successfully", data)


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    data = AuthService(db).login(payload)
    return success_response("Login successful", data)


@router.post("/refresh")
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    data = AuthService(db).refresh(payload)
    return success_response("Token refreshed successfully", data)


@router.post("/logout")
def logout(payload: RefreshRequest, db: Session = Depends(get_db)):
    AuthService(db).logout(payload.refresh_token)
    return success_response("Logout successful")


@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return success_response(
        "Authenticated user retrieved successfully",
        {
            "id": str(current_user.id),
            "full_name": current_user.full_name,
            "email": current_user.email,
            "phone_number": current_user.phone_number,
            "role": current_user.role,
        },
    )


@router.post("/forgot-password")
def forgot_password(payload: dict):
    return success_response(
        "If the account exists, password reset instructions will be sent",
        {"email": payload.get("email")},
    )


@router.post("/reset-password")
def reset_password(payload: dict):
    return success_response("Password reset request accepted", {"token": payload.get("token")})
