from src.data.init import get_db
from sqlalchemy.orm import Session
from sqlalchemy import exc
from src.model.rider import Rider
from error import Missing, Duplicate
from src.data.schemas import RiderBase, RiderStatusUpdate,RiderLogin

def get_all() -> list[RiderBase]:
    db = next(get_db())
    riders = db.query(Rider).all()
    return [RiderBase(**r.__dict__) for r in riders]

def get_one(name: str) -> RiderBase:
    db = next(get_db())
    rider = db.query(Rider).filter(Rider.name == name).first()
    if not rider:
        raise Missing(msg=f"Rider {name} not found")
    return RiderBase(**rider.__dict__)

def create(rider: RiderBase) -> RiderBase:
    if not rider:
        return None

    db = next(get_db())
    db_item = Rider(
        name=rider.name,
        phone_number=rider.phone_number,
        status=rider.status,
        password=rider.password,
        type=rider.type,
        license_plate=rider.license_plate
    )

    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return get_one(db_item.name)
    except exc.IntegrityError:
        db.rollback()
        raise Duplicate(msg="Rider with this name or license plate already exists")

def login(rider_login: RiderLogin) -> RiderBase:
    db = next(get_db())
    rider = db.query(Rider).filter(Rider.phone_number == rider_login.phone_number).first()
    if not rider or rider.password != rider_login.password:
        raise Missing(msg="Invalid phone number or password")
    return RiderBase(**rider.__dict__)

def update_status(rider_id: int, status_update: RiderStatusUpdate) -> RiderBase:
    db = next(get_db())
    rider = db.query(Rider).filter(Rider.id == rider_id).first()
    if not rider:
        raise Missing(msg=f"Rider with ID {rider_id} not found")
    
    rider.status = status_update.status
    db.commit()
    db.refresh(rider)
    return RiderBase(**rider.__dict__)

def accept_ride(user_id: int, rider_id: int) -> RiderBase:
    db = next(get_db())
    rider = db.query(Rider).filter(Rider.id == rider_id).first()
    if not rider:
        raise Missing(msg=f"Rider with ID {rider_id} not found")
    
    rider.status = True  
    db.commit()
    db.refresh(rider)
    return RiderBase(**rider.__dict__)

def delete(rider_id: int) -> bool:
    db = next(get_db())
    rider = db.query(Rider).filter(Rider.id == rider_id).one_or_none()
    if not rider:
        raise Missing(msg="Rider not found")

    db.delete(rider)
    db.commit()
    return True