from fastapi import APIRouter, HTTPException
import src.service.booking as service
from error import Duplicate, Missing
from src.data.schemas import BookingBase

router = APIRouter(prefix="/booking")

@router.get("")
@router.get("/")
def get_all() -> list[BookingBase]:
    return service.get_all()

@router.get("/{booking_id}")
def get_one(booking_id: str) -> BookingBase:
    try:
        return service.get_one(booking_id)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(booking: BookingBase) -> BookingBase:
    try:
        return service.create(booking)
    except Duplicate as exc:
        raise HTTPException(status_code=400, detail=exc.msg)

@router.patch("/{booking_id}")
def modify(booking_id: str, booking: BookingBase) -> BookingBase:
    try:
        return service.modify(booking_id, booking)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete("/{booking_id}", status_code=204)
def delete(booking_id: str):
    try:
        return service.delete(booking_id)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
