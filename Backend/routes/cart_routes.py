from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.cart_model import Cart
from database.db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/cart/add")
def add_to_cart(user_id: int, product_id: int, quantity: int, db: Session = Depends(get_db)):

    cart = Cart(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity
    )

    db.add(cart)
    db.commit()

    return {"message": "Added to cart"}

@router.get("/cart/{user_id}")
def view_cart(user_id: int, db: Session = Depends(get_db)):

    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()

    return cart_items


@router.delete("/cart/remove/{id}")
def remove_from_cart(id: int, db: Session = Depends(get_db)):

    item = db.query(Cart).filter(Cart.id == id).first()

    db.delete(item)
    db.commit()

    return {"message": "Removed from cart"}