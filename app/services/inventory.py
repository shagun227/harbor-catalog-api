from sqlalchemy.orm import Session

from app.schemas import AtpQuery
from app.services.catalog import get_product
from app.services.errors import CatalogError


def receive(session: Session, sku: str, quantity: int) -> int:
    product = get_product(session, sku)
    if product.stock is None:
        raise CatalogError(f"SKU '{sku}' has no stock record", 409)
    product.stock.on_hand += quantity
    session.commit()
    return product.stock.available


def reserve(session: Session, sku: str, quantity: int) -> int:
    product = get_product(session, sku)
    if product.stock is None:
        raise CatalogError(f"SKU '{sku}' has no stock record", 409)
    if product.stock.available < quantity:
        raise CatalogError(
            f"Only {product.stock.available} units of '{sku}' are available",
            409,
        )
    product.stock.reserved += quantity
    session.commit()
    return product.stock.available


def available_to_promise(session: Session, sku: str, quantity: int) -> AtpQuery:
    product = get_product(session, sku)
    available = product.stock.available if product.stock else 0
    return AtpQuery(
        sku=sku,
        requested=quantity,
        available=available,
        can_fulfill=available >= quantity and product.is_active,
    )
