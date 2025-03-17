from fastapi import APIRouter, HTTPException
import src.service.booking as service
from error import Duplicate, Missing
from src.data.schemas import BookingCreate, BookingUpdate, BookingResponse

router = APIRouter(prefix="/booking", tags=["Booking"])

@router.get("/", response_model=list[BookingResponse])
def get_all():
    return service.get_all()

@router.get("/{booking_id}", response_model=BookingResponse)
def get_one(booking_id: int):
    try:
        return service.get_one(booking_id)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post("/", status_code=201, response_model=BookingResponse)
def create(booking: BookingCreate):
    try:
        return service.create(booking)
    except Duplicate as exc:
        raise HTTPException(status_code=400, detail=exc.msg)

@router.patch("/{booking_id}", response_model=BookingResponse)
def modify(booking_id: int, booking: BookingUpdate):
    try:
        return service.modify(booking_id, booking)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete("/{booking_id}", status_code=204)
def delete(booking_id: int):
    try:
        return service.delete(booking_id)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
