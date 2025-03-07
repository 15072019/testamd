from typing import Optional
from src.data.schemas import RiderBase, RiderStatusUpdate
import src.data.rider as data
import httpx

def get_all() -> list[RiderBase]:
    return data.get_all()

def get_one(name: str) -> Optional[RiderBase]: 
    return data.get_one(name)

def create(rider: RiderBase) -> RiderBase:
    return data.create(rider)

def update_status(rider_id: int, status_update: RiderStatusUpdate) -> RiderBase:
    return data.update_status(rider_id, status_update)

def accept_ride(rider_id: int) -> RiderBase:
    return data.accept_ride(rider_id)

def delete(rider_id: int) -> None:  
    data.delete(rider_id)


