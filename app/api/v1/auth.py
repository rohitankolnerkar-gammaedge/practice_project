from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.auth_schema import (
    ChangePasswordRequest,
    TokenResponse,
    UserLogin,
    UserOut,
    UserRegister,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(payload: UserRegister, db: Session = Depends(get_db)):

    AuthService.register_user(
        db=db,
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
    )

    return {"message": "User created successfully"}


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):

    return AuthService.login_user(db=db, email=payload.email, password=payload.password)


@router.get("/me", response_model=UserOut)
def get_me(user=Depends(get_current_user)):
    return user


@router.patch("/me/password")
def change_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return AuthService.change_password(
        db=db,
        user=user,
        current_password=payload.current_password,
        new_password=payload.new_password,
    )
