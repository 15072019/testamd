# ride_matching/services/fare.py

def calculate_fare(distance: float) -> float:
    """Calculate the distance."""
    
    fare = 0

    # 1 km dau tien
    if distance >= 1:
        fare += 10_000
        distance -= 1

    # 2km - 4km tiep theo so voi 1 km dau tien ( tam 3km)
    if distance > 0:
        next_km = min(distance, 3)  
        fare += next_km * 15_000
        distance -= next_km

    # Tren 4km thi tinh gia 12k/km
    if distance > 0:
        fare += distance * 12_000

    return fare
