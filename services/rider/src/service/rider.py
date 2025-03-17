import src.data.rider as data
from src.data.schemas import RiderBase, RiderStatusUpdate

def get_all() -> list[RiderBase]:
    return data.get_all()

def get_one(name: str) -> RiderBase:
    return data.get_one(name)

def create(rider: RiderBase) -> RiderBase:
    return data.create(rider)

def update_status(rider_id: int, status_update: RiderStatusUpdate) -> RiderBase:
    return data.update_status(rider_id, status_update)

def accept_ride(user_id: int, rider_id: int) -> RiderBase:
    return data.accept_ride(user_id, rider_id)

def delete(rider_id: int) -> bool:
    return data.delete(rider_id)