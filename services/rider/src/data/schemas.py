from pydantic import BaseModel

class RiderBase(BaseModel):
    name: str
    phone_number: str  
    password: str     
    status: bool
    rating: float = 5.0
    type: str
    license_plate: str

class RiderLogin(BaseModel):
    phone_number: str
    password: str

class RiderCreate(RiderBase):
    pass

class RiderStatusUpdate(BaseModel):
    status: bool

class Rider(RiderBase):
    id: int

    class Config:
        from_attributes = True
