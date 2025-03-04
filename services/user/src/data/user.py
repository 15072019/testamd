from src.data.init import get_db 
from sqlalchemy.orm import Session
from src.model.user import User
from src.data.schemas import UserBase, UserCreate, Token, UserResponse
from error import Missing, Duplicate
import src.service.user_auth as auth
from contextlib import closing

def create_user(user: UserCreate) -> UserResponse:
    with closing(next(get_db())) as db:
        existing_user = db.query(User).filter(User.phone_number == user.phone_number).first()
        if existing_user:
            raise Duplicate(msg=f"User with phone number {user.phone_number} already exists")
        try:
            hashed_password = auth.hash_password(user.password)  
            db_user = User(
                name=user.name,
                phone_number=user.phone_number,
                password=hashed_password,
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return UserResponse(phone_number=db_user.phone_number)

        except Exception as e:
            db.rollback()
            raise e


# Get a user by phone number
def get_user_by_phone(phone_number: str) -> UserBase:
    with closing(next(get_db())) as db:
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if not user:
            raise Missing(msg=f"User with number {phone_number} not found")
        return UserBase(name=user.name, phone_number=user.phone_number)

# Login a user by validating credentials and returning a token
def login_user(phone_number: str, password: str) -> Token:
    with closing(next(get_db())) as db:
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if not user or not auth.verify_password(password, user.password):  
            raise Missing(msg="Invalid credentials")

        # Create an access token
        access_token = auth.create_access_token(payload={"sub": user.phone_number})
        return Token(access_token=access_token, token_type="bearer")

# Get all users (with optional limit for performance)
def get_all_users(limit: int = 50) -> list[UserBase]:
    with closing(next(get_db())) as db:
        users = db.query(User).limit(limit).all()
        return [UserBase(name=user.name, phone_number=user.phone_number) for user in users]

# Booking a ride
def booking_ride(User_id: int) -> str:
    with closing(next(get_db())) as db:
        user = db.query(User).filter(User.id == User_id).first()
        if not user:
            raise Missing(msg="User not found")
        return "Ride booked successfully!"
