from langchain.tools import tool
from database.db import SessionLocal
from models.product_model import Product
from models.cart_model import Cart
from  models.user_model import User
from sqlalchemy import func

@tool
def search_products(query: str):
    """Search products by name and return product id, name and price"""

    db = SessionLocal()

    products = db.query(Product).filter(
        func.lower(Product.name).contains(query.lower())
    ).all()

    db.close()

    if not products:
        return "No products found"

    return "\n".join(
        [f"id:{p.id}, name:{p.name}, price:{p.price}, stock:{p.stock}" for p in products]
    )


@tool
def add_to_cart(data: str):
    """
    Add product to cart.
    Input format: quantity,user_id,product_id
    Example: "2,1,3"
    """

    quantity, user_id, product_id = data.split(",")

    quantity = int(quantity)
    user_id = int(user_id)
    product_id = int(product_id)

    db = SessionLocal()

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        db.close()
        return "Product does not exist"

    cart = Cart(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity
    )

    db.add(cart)
    db.commit()
    db.refresh(cart)
    db.close()

    return f"{quantity} item(s) added to cart"

@tool
def remove_from_cart(data: str):
    """
    Remove product from cart.
    Input format: 'user_id,product_id'
    """

    user_id, product_id = data.split(",")

    db = SessionLocal()

    cart = db.query(Cart).filter(
        Cart.user_id == int(user_id),
        Cart.product_id == int(product_id)
    ).first()

    if cart:
        db.delete(cart)
        db.commit()

    db.close()

    return "Product removed from cart"















@tool
def view_cart(user_id: str):
    """View all products in the user's cart. Input format: user_id"""

    db = SessionLocal()

    items = db.query(Cart).filter(Cart.user_id == int(user_id)).all()

    if not items:
        db.close()
        return "Cart is empty"

    result = []
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        result.append(
            f"{product.name} | quantity: {item.quantity} | price: {product.price}"
        )

    db.close()

    return "\n".join(result)


# SUCESSFULLY

@tool
def update_cart_quantity(data: str):
    """
    Update quantity of a cart item.
    Input format: user_id,product_id,quantity
    """

    user_id, product_id, quantity = data.split(",")

    db = SessionLocal()

    cart = db.query(Cart).filter(
        Cart.user_id == int(user_id),
        Cart.product_id == int(product_id)
    ).first()

    if not cart:
        db.close()
        return "Item not found in cart"

    cart.quantity = int(quantity)

    db.commit()
    db.close()

    return "Cart updated"


#SUCESSFULLY

@tool
def clear_cart(user_id: str):
    """Remove all items from user cart"""

    db = SessionLocal()

    db.query(Cart).filter(Cart.user_id == int(user_id)).delete()

    db.commit()
    db.close()

    return "Cart cleared"


#   sUCESSFULLY
@tool
def cart_total(user_id: str) -> str:
    """Calculate total price of all items in a user's cart. Input format: user_id"""

    db = SessionLocal()

    cart_items = db.query(Cart).filter(Cart.user_id == int(user_id)).all()

    if not cart_items:
        db.close()
        return "Your cart is empty."

    total = 0
    result = []

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if product:
            quantity = item.quantity if item.quantity is not None else 1
            price = product.price if product.price is not None else 0

            subtotal = price * quantity
            total += subtotal

            result.append(
                f"{product.name} | {quantity} × {price} = {subtotal}"
            )

    db.close()

    details = "\n".join(result)

    return f"Cart Items:\n{details}\n\nTotal Price: {total}"


@tool
def login_user(data: str):
    """
    Login a user.
    Input format: email,password
    Example: rishu@gmail.com,123456
    """

    email, password = data.split(",")

    db = SessionLocal()

    user = db.query(User).filter(User.email == email).first()

    if not user:
        db.close()
        return "User not found"

    if user.password != password:
        db.close()
        return "Invalid password"

    db.close()

    return f"Login successful. Welcome {user.username}"