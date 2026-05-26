from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository


class AuthService:

    @staticmethod
    def register_user(db: Session, email: str, password: str, full_name: str):

        existing_user = UserRepository.get_by_email(db, email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists"
            )

        hashed_password = hash_password(password)

        user = UserRepository.create_user(
            db,
            {
                "email": email,
                "hashed_password": hashed_password,
                "full_name": full_name,
            },
        )

        return user

    @staticmethod
    def login_user(db: Session, email: str, password: str):

        user = UserRepository.get_by_email(db, email)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({"sub": str(user.id)})

        return {"access_token": token}

    @staticmethod
    def change_password(
        db: Session,
        user,
        current_password: str,
        new_password: str,
    ):
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Current password is incorrect")

        hashed_password = hash_password(new_password)
        UserRepository.update_password(db, user, hashed_password)

        return {"message": "Password updated successfully"}
