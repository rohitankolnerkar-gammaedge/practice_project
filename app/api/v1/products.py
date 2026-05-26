from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.services.product import ProductService
from app.db.session import get_db
from app.core.security import get_current_user
from app.core.logger import logger

router = APIRouter(prefix="/products", tags=["Products"])

service = ProductService()


@router.post("/", response_model=ProductOut)
def create_product(
    data: ProductCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return service.create_product(db, data, user.id)


@router.get("/", response_model=list[ProductOut])
def get_products(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    search: Optional[str] = Query(default=None, min_length=1),
    category: Optional[str] = Query(default=None, min_length=1),
):
    return service.list_products(db, user.id, skip, limit, search, category)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    logger.info(f"User requested product {product_id}")
    product = service.get_product(db, product_id, user.id)
    if not product:
        logger.warning(f"Product {product_id} not found")
        raise HTTPException(status_code=404, detail="Product not found")
    logger.info(f"Product {product_id} fetched successfully")
    return product


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    product = service.get_product(db, product_id, user.id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return service.update_product(db, product, data)


@router.delete("/{product_id}")
def delete_product(
    product_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    product = service.get_product(db, product_id, user.id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    service.delete_product(db, product)
    return {"message": "Product deleted successfully"}
