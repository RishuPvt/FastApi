from fastapi import FastAPI
from database.db import engine
from models import user_model, product_model, cart_model
from routes import auth_routes, product_routes, cart_routes , agent_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"] ,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_model.Base.metadata.create_all(bind=engine)
product_model.Base.metadata.create_all(bind=engine)
cart_model.Base.metadata.create_all(bind=engine)


app.include_router(auth_routes.router)
app.include_router(product_routes.router)
app.include_router(cart_routes.router)


app.include_router(agent_routes.router)