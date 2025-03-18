from fastapi import APIRouter, HTTPException
import requests
from src.service import match_service
from error import Missing

router = APIRouter(prefix="/ride-matching", tags=["ride_matching"])

BOOKING_SERVICE_URL = "http://localhost:8003/booking/"

@router.get("/distance/{booking_id}")
def get_ride_distance(booking_id: int) -> dict:
    try:
        booking_response = requests.get(f"{BOOKING_SERVICE_URL}/{booking_id}")

        if booking_response.status_code != 200:
            raise Missing("Booking ID not found")

        booking_data = booking_response.json()
        user_id = booking_data.get("user_id")

        if user_id is None:
            raise Missing("User ID not found in booking data")

        rider_id = match_service.get_nearest_rider(user_id)
        if rider_id is None:
            raise Missing("No available rider found")

        distance = match_service.get_distance(user_id, rider_id)
        if distance is None:
            raise Missing("Cannot find the distance")

        fare = match_service.calculate_fare(distance)

        return {
            "booking_id": booking_id,
            "user_id": user_id,
            "rider_id": rider_id,
            "distance": distance,
            "fare": fare
        }

    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
