from .distance import get_nearest_rider, get_distance, DISTANCE_MATRIX
from .fare import calculate_fare

def match_user_to_rider(user_id: int):
    """Match with nearest rider."""
    rider_id = get_nearest_rider(user_id)
    
    if rider_id is None:
        return {"error": "Cannot find users or riders"}

    distance = get_distance(user_id, rider_id)
    fare = calculate_fare(distance)

    return {
        "user_id": user_id,
        "rider_id": rider_id,
        "distance_km": distance,
        "fare_vnd": fare
    }

