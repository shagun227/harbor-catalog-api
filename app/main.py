from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import Base, make_engine, make_session_factory
from app.routers import categories, health, inventory, products
from app.seed import seed_if_empty
from app.services.errors import CatalogError


def create_app(database_url: str | None = None, seed: bool | None = None) -> FastAPI:
    settings = get_settings()
    url = database_url or settings.database_url
    if url.startswith("sqlite:///./"):
        Path("data").mkdir(exist_ok=True)

    engine = make_engine(url)
    Base.metadata.create_all(engine)
    session_factory = make_session_factory(engine)

    app = FastAPI(
        title="Harbor Catalog API",
        version="1.0.0",
        description="Product catalog and available-to-promise inventory API.",
    )
    app.state.session_factory = session_factory

    @app.exception_handler(CatalogError)
    async def handle_catalog_error(_: Request, exc: CatalogError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    app.include_router(health.router)
    app.include_router(categories.router)
    app.include_router(products.router)
    app.include_router(inventory.router)

    should_seed = settings.seed_on_startup if seed is None else seed
    if should_seed:
        with session_factory() as session:
            seed_if_empty(session)

    return app


app = create_app()
