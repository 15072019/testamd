from src.data.schemas import UserBase
import src.data.user as data
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.model.user import User

# JWT Configuration
SECRET_KEY = "abc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_username_or_phone(db: Session, identifier: str):
    return db.query(User).filter((User.phone == identifier) | (User.username == identifier)).first()

def get_all() -> list[UserBase]:
    return data.get_all()

def get_one(name: str) -> UserBase | None:
    return data.get_one(name)

def create(user: UserBase) -> UserBase:
    return data.create(user)

def replace(user_id: str, user: UserBase) -> UserBase:
    return data.modify(user_id, user)

def modify(user_id: str, user: UserBase) -> UserBase:
    return data.modify(user_id, user)

def delete(user_id: str) -> bool:
    return data.delete(user_id)