from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import src.service.booking as service
from error import Duplicate, Missing
from src.data.schemas import BookingBase, BookingCreate, BookingResponse, BookingUpdate
from src.data.init import get_db

router = APIRouter(prefix="/booking")

@router.get("")
@router.get("/")
def get_all(db: Session = Depends(get_db)) -> list[BookingBase]:
    return service.get_all(db)

@router.get("/{booking_id}")
def get_one(booking_id: int, db: Session = Depends(get_db)) -> BookingBase:
    try:
        return service.get_one(db, booking_id)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(booking: BookingCreate, db: Session = Depends(get_db)) -> BookingBase:
    try:
        return service.create(db, booking)
    except Duplicate as exc:
        raise HTTPException(status_code=400, detail=exc.msg)

@router.patch("/{booking_id}")
def modify(booking_id: int, booking: BookingUpdate, db: Session = Depends(get_db)) -> BookingBase:
    try:
        return service.modify(db, booking_id, booking)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete("/{booking_id}", status_code=204)
def delete(booking_id: int, db: Session = Depends(get_db)):
    try:
        return service.delete(db, booking_id)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
