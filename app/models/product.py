from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False, index=True)

    sku = Column(String(100), unique=True, nullable=False, index=True)

    description = Column(String(500), nullable=True)

    price = Column(Float, nullable=False)

    stock_quantity = Column(Integer, nullable=False, default=0)

    category = Column(String(100), nullable=True)

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    owner = relationship("User", back_populates="products")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
