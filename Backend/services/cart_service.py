from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.models import Cart, Product


def add_to_cart(product_id: int, quantity: int, user_id: int):

    db: Session = SessionLocal()

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return {"error": "Product not found"}

    # check if already in cart
    cart_item = db.query(Cart).filter(
        Cart.product_id == product_id,
        Cart.user_id == user_id
    ).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(cart_item)

    db.commit()

    return {
        "message": "Product added to cart",
        "product_id": product_id,
        "quantity": quantity
    }


def get_cart(user_id: int):

    db: Session = SessionLocal()

    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()

    result = []

    for item in cart_items:

        product = db.query(Product).filter(Product.id == item.product_id).first()

        result.append({
            "product_id": product.id,
            "product_name": product.name,
            "price": product.price,
            "quantity": item.quantity
        })

    return result


def remove_from_cart(product_id: int, user_id: int):

    db: Session = SessionLocal()

    item = db.query(Cart).filter(
        Cart.product_id == product_id,
        Cart.user_id == user_id
    ).first()

    if not item:
        return {"error": "Item not found in cart"}

    db.delete(item)
    db.commit()

    return {"message": "Item removed from cart"}