from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.repositories.user_repository import UserRepository


class AuthService:

    @staticmethod
    def register_user(
        db: Session,
        email: str,
        password: str,
        full_name: str
    ):

        existing_user = UserRepository.get_by_email(
            db,
            email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )

        hashed_password = hash_password(password)

        user = UserRepository.create_user(
            db,
            {
                "email": email,
                "hashed_password": hashed_password,
                "full_name": full_name
            }
        )

        return user

    @staticmethod
    def login_user(
        db: Session,
        email: str,
        password: str
    ):

        user = UserRepository.get_by_email(
            db,
            email
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        if not verify_password(
            password,
            user.hashed_password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        token = create_access_token(
            {"sub": str(user.id)}
        )

        return {
            "access_token": token
        }