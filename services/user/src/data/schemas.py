from pydantic import BaseModel

class UserBase(BaseModel):
    id: int
    name: str
    username: str

class UserCreate(BaseModel):
    username: str
    name: str
    phone: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    phone: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None