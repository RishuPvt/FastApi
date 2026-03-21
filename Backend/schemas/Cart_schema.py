from pydantic import BaseModel
from schemas.product_schema import ProductSchema
class AddToCartRequest(BaseModel):
    user_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int   
    product: ProductSchema

    class Config:
        from_attributes = True