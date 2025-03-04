from fastapi import APIRouter, HTTPException
from src.data.schemas import UserCreate, UserResponse, Token, UserBase, UserLogin
import src.service.user as service
from error import Duplicate, Missing

router = APIRouter(prefix="/user")

# Register a new user
@router.post("/register", status_code=201, response_model=UserResponse)
def register(user: UserCreate):
    try:
        created_user = service.create_user(user)
        return UserResponse(phone_number=created_user.phone_number)  

    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)  
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal Server Error") 


# Login a user and return JWT token
@router.post("/login", response_model=Token)
def login(user_login: UserLogin):  
    try:
        token = service.login_user(user_login.phone_number, user_login.password)
        return token
    except Missing as exc:
        raise HTTPException(status_code=401, detail=exc.msg)

# Get all users 
@router.get("/", response_model=list[UserBase])
def get_all_users():
    try:
        return service.get_all_users()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch users")

# Get user by phone number
@router.get("/{phone_number}", response_model=UserBase)
def get_user(phone_number: str):
    try:
        return service.get_user_by_phone(phone_number)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

# Booking ride by User ID
@router.post("/{user_id}/book_ride")
def book_ride(user_id: int):  
    try:
        message = service.booking_ride(user_id)
        return {"message": message}
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
