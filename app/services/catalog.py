from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models import Category, Product, StockLevel
from app.schemas import ProductCreate, ProductRead, ProductUpdate
from app.services.errors import CatalogError


def create_category(session: Session, slug: str, name: str) -> Category:
    existing = session.scalar(select(Category).where(Category.slug == slug))
    if existing:
        raise CatalogError(f"Category '{slug}' already exists", 409)
    category = Category(slug=slug, name=name)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def list_categories(session: Session) -> list[Category]:
    return list(session.scalars(select(Category).order_by(Category.name)))


def create_product(session: Session, payload: ProductCreate) -> Product:
    category = session.scalar(select(Category).where(Category.slug == payload.category_slug))
    if category is None:
        raise CatalogError(f"Unknown category '{payload.category_slug}'", 404)
    if session.scalar(select(Product).where(Product.sku == payload.sku)):
        raise CatalogError(f"SKU '{payload.sku}' already exists", 409)

    product = Product(
        sku=payload.sku,
        name=payload.name,
        description=payload.description,
        price_cents=payload.price_cents,
        currency=payload.currency.upper(),
        category_id=category.id,
    )
    session.add(product)
    session.flush()
    session.add(StockLevel(product_id=product.id, on_hand=payload.initial_on_hand, reserved=0))
    session.commit()
    return get_product(session, payload.sku)


def get_product(session: Session, sku: str) -> Product:
    product = session.scalar(
        select(Product)
        .where(Product.sku == sku)
        .options(selectinload(Product.category), selectinload(Product.stock))
    )
    if product is None:
        raise CatalogError(f"SKU '{sku}' was not found", 404)
    return product


def update_product(session: Session, sku: str, payload: ProductUpdate) -> Product:
    product = get_product(session, sku)
    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(product, field, value)
    session.commit()
    return get_product(session, sku)


def list_products(
    session: Session,
    *,
    query: str | None,
    category_slug: str | None,
    page: int,
    page_size: int,
) -> tuple[list[Product], int]:
    statement = select(Product).options(selectinload(Product.category), selectinload(Product.stock))
    count_statement = select(func.count(Product.id))

    if query:
        like = f"%{query.lower()}%"
        statement = statement.where(func.lower(Product.name).like(like))
        count_statement = count_statement.where(func.lower(Product.name).like(like))
    if category_slug:
        statement = statement.join(Category).where(Category.slug == category_slug)
        count_statement = count_statement.join(Category).where(Category.slug == category_slug)

    total = session.scalar(count_statement) or 0
    offset = (page - 1) * page_size
    items = list(
        session.scalars(statement.order_by(Product.name).offset(offset).limit(page_size))
    )
    return items, total


def to_product_read(product: Product) -> ProductRead:
    available = product.stock.available if product.stock else 0
    return ProductRead(
        sku=product.sku,
        name=product.name,
        description=product.description,
        price_cents=product.price_cents,
        currency=product.currency,
        category_slug=product.category.slug,
        is_active=product.is_active,
        available=available,
        created_at=product.created_at,
    )
