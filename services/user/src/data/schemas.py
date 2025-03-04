from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    phone_number: str

class UserCreate(UserBase):
    password: str  


class UserResponse(BaseModel):  
    phone_number: str  

    class Config:
        from_attributes = True  


class UserLogin(BaseModel):
    phone_number: str
    password: str  


class Token(BaseModel):
    access_token: str
    token_type: str  
