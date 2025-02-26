from fastapi import APIRouter, FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import src.service.user as service
from error import Duplicate, Missing
from src.data.schemas import UserBase, UserCreate, UserResponse, Token
from src.model.user import User
from src.data import get_db
from src.service.user import hash_password, create_access_token, verify_password, get_user_by_username_or_phone
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/user")

@router.get("")
@router.get("/")
def get_all() -> list[UserBase]:
    return service.get_all()

@router.get("/{name}")
def get_one(name) -> UserBase:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(user: UserBase) -> UserBase:
    try:
        return service.create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.patch("/{user_id}")
def modify(user_id: str, user: UserBase) -> UserBase:
    try:
        return service.modify(user_id, user)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete("/{user_id}", status_code=204)
def delete(user_id: str):
    try:
        return service.delete(user_id)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# User Registration
@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        name=user.name,
        phone=user.phone,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# User Login
@app.post("/login", response_model=Token)
def login_for_access_token(identifier: str, password: str, db: Session = Depends(get_db)):
    user = get_user_by_username_or_phone(db, identifier)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Dependency to get the current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    user = get_user_by_username_or_phone(db, username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Protected Route (Get Current User Info)
@app.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user