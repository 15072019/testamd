from fastapi import APIRouter, HTTPException
from src.services import match_service  # Import lại theo kiểu package
from error import Missing

router = APIRouter(prefix="/ride-matching")

@router.get("/distance/{user_id}/{rider_id}")
def get_ride_distance(user_id: str, rider_id: str) -> dict:
    try:
        distance = match_service.get_distance(user_id, rider_id)
        if distance is None:
            raise Missing("Cannot find the distance")
        return {"user_id": user_id, "rider_id": rider_id, "distance": distance}
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.get("/fare/{distance}")
def get_ride_fare(distance: int) -> dict:
    return {"distance": distance, "fare": match_service.calculate_fare(distance)}

@router.get("/match/{user_id}")
def match_rider(user_id: str) -> dict:
    try:
        result = match_service.match_user_to_rider(user_id)
        if "error" in result:
            raise Missing(result["error"])
        return result
    except Missing as exc:
        raise HTTPException(status_code=400, detail=exc.msg)
