from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.products import router as product_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(product_router)
