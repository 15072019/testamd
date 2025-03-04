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

RIDER_SERVICE_URL = "http://localhost:8002"  

def get_rider_by_id(rider_id: int):
    url = f"{RIDER_SERVICE_URL}/riders/{rider_id}"  
    try:
        response = httpx.get(url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP (404, 500, ...)
        return response.json()  # Trả về dữ liệu JSON của rider
    except httpx.RequestError as e:
        print(f"Error connecting to Rider service: {e}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"Rider service returned an error: {e.response.status_code}")
        return None
