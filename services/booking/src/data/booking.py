from enum import Enum
from src.data.init import get_db
from src.model.booking import Booking
from error import Missing, Duplicate
from sqlalchemy import exc
from src.data.schemas import BookingBase, BookingStatus

def get_all() -> list[BookingBase]:
    db = next(get_db())
    return db.query(Booking).all()

def get_one(booking_id: int) -> BookingBase:
    db = next(get_db())
    row = db.query(Booking).filter(Booking.id == booking_id).first()
    if row:
        return row
    else:
        raise Missing(msg=f"Booking ID {booking_id} not found")

def create(booking: BookingBase) -> BookingBase:
    if not booking:
        return None

    db = next(get_db())

    user_exists = db.execute(f"SELECT id FROM users WHERE id = {booking.user_id}").fetchone()
    if not user_exists:
        raise Missing(msg=f"User ID {booking.user_id} not found")

    if booking.rider_id:
        rider_exists = db.execute(f"SELECT id FROM riders WHERE id = {booking.rider_id}").fetchone()
        if not rider_exists:
            raise Missing(msg=f"Rider ID {booking.rider_id} not found")

    db_item = Booking(
        user_id=booking.user_id,
        rider_id=booking.rider_id,
        status=BookingStatus.PENDING,
        fare_estimate=booking.fare_estimate
    )

    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return get_one(db_item.id)
    except exc.IntegrityError:
        raise Duplicate(msg=f"Booking with this ID already exists")

def modify(booking_id: int, booking: BookingBase) -> BookingBase:
    if not (booking_id and booking):
        return None

    db = next(get_db())
    item = db.query(Booking).filter(Booking.id == booking_id).one_or_none()

    if item:
        for var, value in vars(booking).items():
            if var == "status" and value and value not in BookingStatus.__members__.values():
                raise ValueError(f"Invalid booking status: {value}")
            setattr(item, var, value) if value else None

        db.add(item)
        db.commit()
        db.refresh(item)
        return get_one(item.id)
    else:
        raise Missing(msg=f"Booking ID {booking_id} not found")

def delete(booking_id: int) -> bool:
    if not booking_id:
        return False

    db = next(get_db())
    item = db.query(Booking).filter(Booking.id == booking_id).one_or_none()

    if item:
        db.delete(item)
        db.commit()
        return True
    else:
        raise Missing(msg=f"Booking ID {booking_id} not found")
