from src.data.schemas import UserBase
import src.data.user as data

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