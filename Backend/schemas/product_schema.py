from pydantic import BaseModel

class ProductSchema(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int

    class Config:
        from_attributes = True   # ✅ for SQLAlchemy (IMPORTANT)