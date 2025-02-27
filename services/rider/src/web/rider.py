from fastapi import APIRouter, HTTPException
from src.data.schemas import RiderBase, RiderStatusUpdate, RiderLogin
from src.model.rider import Rider
import src.service.rider as service
import src.service.auth as auth
from error import Duplicate, Missing

router = APIRouter(prefix="/rider")

@router.post("/register", status_code=201)
def register(rider: RiderBase):
    try:
        return auth.register_rider(rider)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)

@router.post("/login")
def login(rider_login: RiderLogin):
    try:
        return auth.login_rider(rider_login)
    except Missing as exc:
        raise HTTPException(status_code=401, detail=exc.msg)

@router.get("/")
def get_all() -> list[RiderBase]:
    return service.get_all()

@router.get("/{name}")
def get_one(name: str) -> RiderBase:
    try: 
        rider = service.get_one(name)
        if not rider:
            raise HTTPException(status_code=404, detail=f"Rider with name {name} not found")
        return rider
    except Missing as exc: 
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post("/", status_code=201)
def create(rider: RiderBase) -> RiderBase:
    try:
        return service.create(rider)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)

@router.put("/{rider_id}")
def update_status(rider_id: int, status_update: RiderStatusUpdate) -> RiderBase:
    try:
        updated_rider = service.update_status(rider_id, status_update)  # ✅ Ensure correct function name
        if not updated_rider:
            raise HTTPException(status_code=404, detail=f"Rider with ID {rider_id} not found")
        return updated_rider
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.put("/{rider_id}/accept_ride")
def accept_ride(rider_id: int) -> RiderBase:
    try:
        return service.accept_ride(rider_id)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete("/{rider_id}", status_code=204)
def delete(rider_id: int):
    try:
        service.delete(rider_id)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
