from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.user_model import User
from utils.config import SECRET_KEY , ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    
    print("TOKEN RECEIVED:", token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print("PAYLOAD:", payload)    # 👈 ADD THIS
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError as e:
      print("JWT ERROR:", str(e))  # 👈 this will print "Signature has expired"
      raise HTTPException(status_code=401, detail="Token invalid")