from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import User

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "FastAPI + SQLite + Alembic"}


@app.get("/users")
def get_users():
    db: Session = SessionLocal()

    users = db.query(User).all()

    result = []

    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })

    db.close()

    return result