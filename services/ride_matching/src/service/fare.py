def calculate_fare(distance: float) -> float:
    """Tính giá tiền dựa trên khoảng cách."""
    
    fare = 0

    # 1 km đầu tiên
    if distance >= 1:
        fare += 10_000
        distance -= 1

    # 2km - 4km tiếp theo (tối đa 3km)
    if distance > 0:
        next_km = min(distance, 3)  
        fare += next_km * 15_000
        distance -= next_km

    # Trên 4km thì tính 12k/km
    if distance > 0:
        fare += distance * 12_000

    return fare
