from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


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


class UserBasic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sku: str
    description: Optional[str]
    price: float
    stock_quantity: int
    category: Optional[str]

    owner_id: int
    owner: UserBasic
