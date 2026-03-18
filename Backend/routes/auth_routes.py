from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.user_model import User
from utils.auth import hash_password
from fastapi import HTTPException
from utils.auth import verify_password, create_access_token
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(username: str, email: str, password: str, db: Session = Depends(get_db)):

    hashed_password = hash_password(password)

    user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully"}


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_access_token(
        {"user_id": user.id}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }