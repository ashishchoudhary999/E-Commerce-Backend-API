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

def add_to_cart(db: Session, user_id: int, item: schemas.CartItemCreate):
    product = db.query(models.Product).filter(
        models.Product.id == item.product_id  
    ).first()

    if product is None:
        return None
    
    existing = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id,
        models.CartItem.product_id == item.product_id 
    ).first()

    if existing:
        existing.quantity += item.quantity
        db.commit()
        db.refresh(existing)
        return existing


    new_item = models.CartItem(
        user_id=user_id,
        product_id=item.product_id,
        quantity=item.quantity
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def get_cart(db: Session, user_id: int):
    cart_items = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id
    ).all()

    items = []
    total = 0

    for cart_item in cart_items:
        product = db.query(models.Product).filter(
            models.Product.id == cart_item.product_id
        ).first()

        subtotal = product.price * cart_item.quantity
        total += subtotal

        items.append({
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": cart_item.quantity,
            "subtotal": subtotal
        })

    return {"items": items, "total": total}

def update_cart_item(db: Session, user_id: int, product_id: int, quantity: int):
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id,
        models.CartItem.product_id == product_id
    ).first()

    if cart_item is None:
        return None

    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

def remove_from_cart(db: Session, user_id: int, product_id: int):
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id,
        models.CartItem.product_id == product_id
    ).first()

    if cart_item is None:
        return None

    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}

def place_order(db: Session, user_id: int):
    cart_items = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id
    ).all()

    if not cart_items:
        return None
    
    total_price = 0
    order_items_data = []

    for cart_item in cart_items:
        product = db.query(models.Product).filter(
            models.Product.id == cart_item.product_id
        ).first()

        if product.stock <cart_item.quantity:
            return {"error": f"Not enough stock for {product.name}"}

        subtotal = product.price * cart_item.quantity
        total_price += subtotal

        order_items_data.append({
            "product": product,
            "quantity": cart_item.quantity,
            "price": product.price
        })
    
    new_order = models.Order(
        user_id=user_id,
        total_price=total_price,
        status="pending"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for data in order_items_data:
        order_item = models.OrderItem(
            order_id=new_order.id,
            product_id=data["product"].id,
            quantity=data["quantity"],
            price_at_purchase=data["price"]
        )
        db.add(order_item)

        data["product"].stock -= data["quantity"]

    for cart_item in cart_items:
        db.delete(cart_item)

    db.commit()
    db.refresh(new_order)
    return new_order

def get_my_orders(db: Session, user_id: int):
    return db.query(models.Order).filter(
        models.Order.user_id == user_id
    ).all()

def cancel_order(db: Session, user_id: int, order_id: int):
    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == user_id
    ).first()

    if order is None:
        return None

    if order.status != "pending":
        return {"error": "Only pending orders can be cancelled"}

    order.status = "cancelled"
    db.commit()
    db.refresh(order)
    return order
