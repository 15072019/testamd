from pydantic import BaseModel
from enum import Enum

# Define Booking Status Enum
class BookingStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    COMPLETE = "complete"
    CANCELLED = "cancelled"


class BookingBase(BaseModel):
    status: BookingStatus
    phone: str
    fare_estimate: float
    user_id: int
    rider_id: int | None = None
    class Config:
        from_attributes = True 

class BookingCreate(BaseModel):
    phone: str
    fare_estimate: float
    user_id: int
    rider_id: int | None = None
    status: BookingStatus = BookingStatus.PENDING  # Default là "pending"


class BookingUpdate(BaseModel):
    status: BookingStatus | None = None  
    rider_id: int | None = None  


class BookingResponse(BaseModel):
    id: int
    phone: str
    fare_estimate: float
    status: BookingStatus
    user_id: int
    rider_id: int | None

    class Config:
        from_attributes = True
