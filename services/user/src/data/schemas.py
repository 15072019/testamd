from pydantic import BaseModel

class UserBase(BaseModel):
    user_id: int
    name: str
    username: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True