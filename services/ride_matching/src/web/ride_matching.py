from fastapi import APIRouter, HTTPException
import src.services.match_service as service
from error import Missing

router = APIRouter(prefix="/ride-matching")

@router.get("/distance/{user_id}/{rider_id}")
def get_ride_distance(user_id: str, rider_id: str) -> dict:
    try:
        distance = service.get_distance(user_id, rider_id)
        if distance is None:
            raise Missing("Không tìm thấy khoảng cách")
        return {"user_id": user_id, "rider_id": rider_id, "distance": distance}
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.get("/fare/{distance}")
def get_ride_fare(distance: int) -> dict:
    return {"distance": distance, "fare": service.calculate_fare(distance)}

@router.get("/match/{user_id}")
def match_rider(user_id: str) -> dict:
    try:
        result = service.match_user_to_rider(user_id)
        if "error" in result:
            raise Missing(result["error"])
        return result
    except Missing as exc:
        raise HTTPException(status_code=400, detail=exc.msg)
