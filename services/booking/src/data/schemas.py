from pydantic import BaseModel
from typing import Optional

class BookingBase(BaseModel):
    id: int
    status: str
    phone: str
    fare_estimate: float
    user_id: int
    rider_id: Optional[int] = None

class BookingCreate(BaseModel):
    phone: str
    fare_estimate: float
    user_id: int
    rider_id: Optional[int] = None
    status: str = "pending" # con de set 4 cai status kia thi hong bit, chac ghi chay

class BookingResponse(BaseModel):
    id: int
    phone: str
    fare_estimate: float
    status: str
    user_id: int
    rider_id: Optional[int]

    class Config:
        from_attributes = True
