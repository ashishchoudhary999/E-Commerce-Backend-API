from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas
from ..auth import get_current_user
from ..models import User

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/")
def add_to_cart(
    item: schemas.CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = crud.add_to_cart(db, current_user.id, item)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Item added to cart"}

@router.get("/", response_model=schemas.CartResponse)
def view_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_cart(db, current_user.id)

@router.put("/{product_id}")
def update_cart(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    result = crud.update_cart_item(db, current_user.id, product_id, quantity)
    if result is None:
        raise HTTPException(status_code=404, detail="product not found")
    return {"message": "Cart updated"}

@router.delete("/{product_id}")
def delete_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    result = crud.remove_from_cart(db, current_user.id, product_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    return {"messaage": "Item removed from cart"}