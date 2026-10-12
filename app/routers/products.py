from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.deps import get_session
from app.schemas import Page, ProductCreate, ProductRead, ProductUpdate
from app.services.catalog import (
    create_product,
    get_product,
    list_products,
    to_product_read,
    update_product,
)

router = APIRouter(prefix="/api/v1/products", tags=["products"])


@router.get("", response_model=Page)
def index(
    q: str | None = None,
    category: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
) -> Page:
    items, total = list_products(
        session, query=q, category_slug=category, page=page, page_size=page_size
    )
    return Page(
        items=[to_product_read(item) for item in items],
        page=page,
        page_size=page_size,
        total=total,
    )


@router.post("", response_model=ProductRead, status_code=201)
def create(payload: ProductCreate, session: Session = Depends(get_session)) -> ProductRead:
    return to_product_read(create_product(session, payload))


@router.get("/{sku}", response_model=ProductRead)
def show(sku: str, session: Session = Depends(get_session)) -> ProductRead:
    return to_product_read(get_product(session, sku))


@router.patch("/{sku}", response_model=ProductRead)
def update(
    sku: str, payload: ProductUpdate, session: Session = Depends(get_session)
) -> ProductRead:
    return to_product_read(update_product(session, sku, payload))
