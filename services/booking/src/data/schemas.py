from pydantic import BaseModel
from typing import Optional
from enum import Enum

class BookingStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    CANCELED = "canceled"
    COMPLETED = "completed"

class BookingBase(BaseModel):
    status: BookingStatus 
    fare_estimate: Optional[float] = None
    user_id: int
    rider_id: Optional[int] = None
    distance: float

class BookingCreate(BaseModel):
    status: BookingStatus
    user_id: int
    distance: float

class BookingUpdate(BaseModel):
    status: Optional[BookingStatus] = None
    distance: Optional[float] = None

class BookingResponse(BookingBase):
    id: int

    class Config:
        from_attributes = True
