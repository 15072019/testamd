from src.data.schemas import BookingBase, BookingCreate, BookingResponse, BookingStatus
import src.data.booking as data
from sqlalchemy.orm import Session

def calculate_fare(distance: float) -> float:    
    fare = 0

    if distance >= 1:
        fare += 10_000
        distance -= 1

    if distance > 0:
        next_km = min(distance, 3)  
        fare += next_km * 15_000
        distance -= next_km

    if distance > 0:
        fare += distance * 12_000

    return fare

def get_all() -> list[BookingBase]:
    return data.get_all()

def get_one(booking_id: int) -> BookingBase | None:
    return data.get_one(booking_id)

def create(booking: BookingCreate) -> BookingBase:
    fare_estimate = calculate_fare(booking.distance)  
    booking_data = BookingBase(
        status=booking.status,
        fare_estimate=fare_estimate,
        user_id=booking.user_id,
        rider_id=None,  
        distance=booking.distance,
    )
    return data.create(booking_data)

def modify(booking_id: int, booking: BookingBase) -> BookingBase:
    return data.modify(booking_id, booking)

def delete(booking_id: int) -> bool:
    return data.delete(booking_id)
