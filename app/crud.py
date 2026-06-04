from sqlalchemy.orm import Session
from . import models, schemas

def create_product(db: Session, product: schemas.ProductCreate):
    new_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category=product.category
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_products(db: Session):
    return db.query(models.Product).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

def update_product(db: Session, product_id: int, updated: schemas.ProductCreate):
    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if product is None:
        return None
    
    product.name = updated.name
    product.description = updated.description
    product.price = updated.price
    product.stock = updated.stock
    product.category = updated.category

    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if product is None:
        return None

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
