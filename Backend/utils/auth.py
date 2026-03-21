from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from utils.config import ALGORITHM , SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



# hash password
def hash_password(password: str):
    return pwd_context.hash(password)


# verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# create jwt token
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=7)

    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token

