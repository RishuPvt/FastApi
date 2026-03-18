from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.product_model import Product

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


@router.post("/admin/add-product")
def add_product(
    name: str,
    description: str,
    price: float,
    stock: int,
    db: Session = Depends(get_db)
):

    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


@router.put("/admin/update-product/{id}")
def update_product(id: int, price: float, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == id).first()

    product.price = price

    db.commit()

    return product


@router.delete("/admin/delete-product/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == id).first()

    db.delete(product)
    db.commit()

    return {"message": "Product deleted"}