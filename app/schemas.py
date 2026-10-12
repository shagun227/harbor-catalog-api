from datetime import datetime

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    slug: str = Field(min_length=2, max_length=80, pattern=r"^[a-z0-9-]+$")
    name: str = Field(min_length=2, max_length=120)


class CategoryRead(BaseModel):
    id: int
    slug: str
    name: str

    model_config = {"from_attributes": True}


class ProductCreate(BaseModel):
    sku: str = Field(min_length=2, max_length=64)
    name: str = Field(min_length=2, max_length=200)
    description: str = ""
    price_cents: int = Field(ge=0)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    category_slug: str
    initial_on_hand: int = Field(default=0, ge=0)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = None
    price_cents: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class ProductRead(BaseModel):
    sku: str
    name: str
    description: str
    price_cents: int
    currency: str
    category_slug: str
    is_active: bool
    available: int
    created_at: datetime


class Page(BaseModel):
    items: list[ProductRead]
    page: int
    page_size: int
    total: int


class ReceiveRequest(BaseModel):
    quantity: int = Field(gt=0)


class ReserveRequest(BaseModel):
    quantity: int = Field(gt=0)


class AtpQuery(BaseModel):
    sku: str
    requested: int
    available: int
    can_fulfill: bool
