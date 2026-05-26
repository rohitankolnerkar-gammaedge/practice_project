from sqlalchemy.orm import Session

from app.repositories.product import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self):
        self.repo = ProductRepository()

    def create_product(self, db: Session, data: ProductCreate, owner_id: int):
        return self.repo.create(db, data, owner_id)

    def list_products(
        self,
        db: Session,
        owner_id: int,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
        category: str | None = None,
    ):
        return self.repo.get_all(db, owner_id, skip, limit, search, category)

    def get_product(self, db: Session, product_id: int, owner_id: int):
        return self.repo.get_by_id(db, product_id, owner_id)

    def update_product(self, db: Session, product, data: ProductUpdate):
        return self.repo.update(db, product, data)

    def delete_product(self, db: Session, product):
        return self.repo.delete(db, product)
