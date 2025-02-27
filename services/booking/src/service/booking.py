from src.data.schemas import BookingBase
import src.data.booking as data
from sqlalchemy.orm import Session
from src.model.booking import Booking

def get_all() -> list[BookingBase]:
    return data.get_all()

def get_one(booking_id: int) -> BookingBase | None:
    return data.get_one(booking_id)

def create(booking: BookingBase) -> BookingBase:
    return data.create(booking)

def replace(booking_id: int, booking: BookingBase) -> BookingBase:
    return data.modify(booking_id, booking)

def modify(booking_id: int, booking: BookingBase) -> BookingBase:
    return data.modify(booking_id, booking)

def delete(booking_id: int) -> bool:
    return data.delete(booking_id)
