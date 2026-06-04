from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import crud, schemas
from ..auth import require_admin
from ..models import User

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[schemas.ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

@router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_one_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=schemas.ProductResponse)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return crud.create_product(db, product)

@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int,
    updated: schemas.ProductCreate, 
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    result = crud.update_product(db, product_id, updated)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return result

@router.delete("/{product_id}")
def delete_product(
    product_id: int, 
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    result = crud.delete_product(db, product_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return result 