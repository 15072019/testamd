from src.data.schemas import UserCreate, UserResponse, Token, UserBase
import src.data.user as data

# Get all users
def get_all_users() -> list[UserBase]:  
    return data.get_all_users()

# Get user by phone number
def get_user_by_phone(phone_number: str) -> UserBase:  
    return data.get_user_by_phone(phone_number)

# Create a user
def create_user(user: UserCreate) -> UserResponse:
    created_user = data.create_user(user)
    return UserResponse(phone_number=created_user.phone_number) 

# Login user and return token
def login_user(phone_number: str, password: str) -> Token:
    return data.login_user(phone_number, password)
