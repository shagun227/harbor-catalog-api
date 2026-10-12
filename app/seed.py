from sqlalchemy.orm import Session

from app.schemas import ProductCreate
from app.services.catalog import create_category, create_product, list_categories


def seed_if_empty(session: Session) -> None:
    if list_categories(session):
        return

    create_category(session, "frames", "Frames")
    create_category(session, "lenses", "Lenses")
    create_product(
        session,
        ProductCreate(
            sku="FRAME-100",
            name="Harbor Round Frame",
            description="Acetate round frame.",
            price_cents=890000,
            currency="INR",
            category_slug="frames",
            initial_on_hand=24,
        ),
    )
    create_product(
        session,
        ProductCreate(
            sku="LENS-200",
            name="Clear Daily Lens",
            description="30-pack daily disposable lenses.",
            price_cents=149000,
            currency="INR",
            category_slug="lenses",
            initial_on_hand=80,
        ),
    )
