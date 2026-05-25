from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.auth_schema import (
    UserRegister,
    UserLogin,
    TokenResponse
)

from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    payload: UserRegister,
    db: Session = Depends(get_db)
):

    AuthService.register_user(
        db=db,
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name
    )

    return {
        "message": "User created successfully"
    }


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    payload: UserLogin,
    db: Session = Depends(get_db)
):

    return AuthService.login_user(
        db=db,
        email=payload.email,
        password=payload.password
    )