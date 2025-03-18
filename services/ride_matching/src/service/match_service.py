from .distance import get_nearest_rider, get_distance
from .fare import calculate_fare

def match_user_to_rider(user_id: int):
    """Tìm rider gần nhất và tính giá tiền."""
    rider_id = get_nearest_rider(user_id)
    
    if rider_id is None:
        return {"error": "No available rider found"}

    distance = get_distance(user_id, rider_id)
    if distance is None:
        return {"error": "Cannot determine distance"}

    fare = calculate_fare(distance)

    return {
        "user_id": user_id,
        "rider_id": rider_id,
        "distance_km": distance,
        "fare_vnd": fare
    }
