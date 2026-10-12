from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_session
from app.schemas import CategoryCreate, CategoryRead
from app.services.catalog import create_category, list_categories

router = APIRouter(prefix="/api/v1/categories", tags=["categories"])


@router.get("", response_model=list[CategoryRead])
def index(session: Session = Depends(get_session)) -> list[CategoryRead]:
    return [CategoryRead.model_validate(item) for item in list_categories(session)]


@router.post("", response_model=CategoryRead, status_code=201)
def create(payload: CategoryCreate, session: Session = Depends(get_session)) -> CategoryRead:
    category = create_category(session, payload.slug, payload.name)
    return CategoryRead.model_validate(category)
