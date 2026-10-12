from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.deps import get_session
from app.schemas import AtpQuery, ReceiveRequest, ReserveRequest
from app.services.inventory import available_to_promise, receive, reserve

router = APIRouter(prefix="/api/v1/inventory", tags=["inventory"])


@router.post("/{sku}/receive")
def receive_stock(
    sku: str, payload: ReceiveRequest, session: Session = Depends(get_session)
) -> dict[str, int | str]:
    available = receive(session, sku, payload.quantity)
    return {"sku": sku, "available": available}


@router.post("/{sku}/reserve")
def reserve_stock(
    sku: str, payload: ReserveRequest, session: Session = Depends(get_session)
) -> dict[str, int | str]:
    available = reserve(session, sku, payload.quantity)
    return {"sku": sku, "available": available}


@router.get("/{sku}/atp", response_model=AtpQuery)
def atp(
    sku: str,
    quantity: int = Query(ge=1),
    session: Session = Depends(get_session),
) -> AtpQuery:
    return available_to_promise(session, sku, quantity)
