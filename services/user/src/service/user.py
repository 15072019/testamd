from src.data.schemas import UserCreate, UserResponse, Token, UserBase
import src.data.user as data

# Get all users
def get_all_users() -> list[UserBase]:  # Changed from UserResponse to UserBase
    return data.get_all_users()

# Get user by phone number
def get_user_by_phone(phone_number: str) -> UserBase:  # Changed from UserResponse to UserBase
    return data.get_user_by_phone(phone_number)

# Create a user
def create_user(user: UserCreate) -> UserResponse:
    created_user = data.create_user(user)
    return UserResponse(phone_number=created_user.phone_number)  # Avoid exposing password

# Login user and return token
def login_user(phone_number: str, password: str) -> Token:
    return data.login_user(phone_number, password)

# Book a ride using user_id instead of phone_number
def booking_ride(user_id: int) -> str:  # Changed from phone_number to user_id
    return data.booking_ride(user_id)
