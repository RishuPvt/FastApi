from sqlalchemy import Column, Integer, ForeignKey
from database.db import Base
from sqlalchemy.orm import relationship
class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    quantity = Column(Integer, default=1, nullable=False)
    product = relationship("Product") 