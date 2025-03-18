from src.data.init import get_db
from src.model.rider import Rider
from src.data.schemas import RiderBase, RiderLogin
from error import Missing, Duplicate
from passlib.context import CryptContext
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def register_rider(rider: RiderBase) -> RiderBase:
    db = next(get_db())
    
    existing_rider = db.query(Rider).filter(Rider.phone_number == rider.phone_number).first()
    if existing_rider:
        raise Duplicate(msg="Phone number already registered")

    new_rider = Rider(
        name=rider.name,
        phone_number=rider.phone_number,
        password=hash_password(rider.password),  # Hash password before storing
        status=rider.status,
        type=rider.type,
        license_plate=rider.license_plate
    )

    db.add(new_rider)
    db.commit()
    db.refresh(new_rider)
    return RiderBase(**new_rider.__dict__)

def login_rider(rider_login: RiderLogin) -> RiderBase:
    db = next(get_db())
    rider = db.query(Rider).filter(Rider.phone_number == rider_login.phone_number).first()
    
    if not rider or not verify_password(rider_login.password, rider.password):
        raise Missing(msg="Invalid phone number or password")
    
    return RiderBase(**rider.__dict__)  # Return rider info (excluding password)

