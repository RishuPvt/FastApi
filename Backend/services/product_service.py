from database.db import SessionLocal
from database.models import Product

def get_products():

    db = SessionLocal()

    return db.query(Product).all()