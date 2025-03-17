from src.data.init import get_db
from src.model.booking import Booking
from error import Missing, Duplicate
from sqlalchemy import exc, text
from src.data.schemas import BookingBase, BookingStatus, BookingCreate


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

def create(booking: BookingCreate) -> BookingCreate:
    
    if not booking:
        return None

    db = next(get_db())
    
    existing_booking = db.query(Booking).filter(Booking.user_id == booking.user_id).first()
    if existing_booking:
        raise Duplicate(msg=f"User ID {booking.user_id} already has a booking.")

    db_item = Booking(
        user_id=booking.user_id,
        status=BookingStatus.PENDING,
        distance = booking.distance
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
