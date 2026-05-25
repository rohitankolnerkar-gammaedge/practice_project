from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    sku: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    category: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    stock_quantity: Optional[int] = Field(default=None, ge=0)
    category: Optional[str] = None


class ProductOut(BaseModel):
    id: int
    name: str
    sku: str
    description: Optional[str]
    price: float
    stock_quantity: int
    category: Optional[str]

    class Config:
        from_attributes = True
