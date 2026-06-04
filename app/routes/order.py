from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import crud, schemas
from ..auth import get_current_user
from ..models import User

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=schemas.OrderResponse)
def place_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = crud.place_order(db, current_user.id)

    if result is None:
        raise HTTPException(status_code=400, detail="Cart is empty")

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result

@router.get("/", response_model=List[schemas.OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_my_orders(db, current_user.id)

@router.put("/{order_id}/cancel")
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = crud.cancel_order(db, current_user.id, order_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Order not found")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result