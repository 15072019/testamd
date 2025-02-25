from fastapi import APIRouter, HTTPException
import src.service.user as service
from error import Duplicate, Missing
from src.data.schemas import UserBase

router = APIRouter(prefix="/user")

@router.get("")
@router.get("/")
def get_all() -> list[UserBase]:
    return service.get_all()

@router.get("/{name}")
def get_one(name) -> UserBase:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(user: UserBase) -> UserBase:
    try:
        return service.create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.patch("/{user_id}")
def modify(user_id: str, user: UserBase) -> UserBase:
    try:
        return service.modify(user_id, user)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete("/{user_id}", status_code=204)
def delete(user_id: str):
    try:
        return service.delete(user_id)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)