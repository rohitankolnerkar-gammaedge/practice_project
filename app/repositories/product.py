from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:

    def create(self, db: Session, data: ProductCreate, owner_id: int):
        product = Product(**data.model_dump(), owner_id=owner_id)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def get_all(
        self,
        db: Session,
        owner_id: int,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
        category: str | None = None,
    ):
        query = db.query(Product).filter(Product.owner_id == owner_id)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Product.name.ilike(search_pattern),
                    Product.sku.ilike(search_pattern),
                    Product.description.ilike(search_pattern),
                )
            )

        if category:
            query = query.filter(Product.category.ilike(category))

        return query.offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, product_id: int, owner_id: int):
        return (
            db.query(Product)
            .filter(Product.id == product_id, Product.owner_id == owner_id)
            .first()
        )

    def update(self, db: Session, product: Product, data: ProductUpdate):
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)

        db.commit()
        db.refresh(product)
        return product

    def delete(self, db: Session, product: Product):
        db.delete(product)
        db.commit()
