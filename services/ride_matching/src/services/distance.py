import random

DISTANCE_MATRIX = [
    [8, 5, 6, 2, 7],  # User_1 -> Riders
    [3, 9, 4, 6, 1],  # User_2 -> Riders
    [5, 2, 8, 7, 4],  # User_3 -> Riders
    [6, 10, 3, 1, 9], # User_4 -> Riders
    [7, 4, 2, 9, 5]   # User_5 -> Riders
]

def get_distance(user_id: int, rider_id: int) -> int | None:
    try:
        user_id = int(user_id)
        rider_id = int(rider_id)
    except ValueError:
        return None  

    if user_id < 1 or user_id > len(DISTANCE_MATRIX):
        return None  
    if rider_id < 1 or rider_id > len(DISTANCE_MATRIX[0]):
        return None  

    return DISTANCE_MATRIX[user_id - 1][rider_id - 1]

def get_nearest_rider(user_id: int) -> int | None:
    try:
        user_id = int(user_id)
    except ValueError:
        return None  

    if user_id < 1 or user_id > len(DISTANCE_MATRIX):
        return None  

    user_index = user_id - 1
    distances = DISTANCE_MATRIX[user_index]

    min_distance = min(distances)

    nearest_riders = []
    for i in range(len(distances)):
        if distances[i] == min_distance:
            nearest_riders.append(i + 1)  

    if nearest_riders:
        return random.choice(nearest_riders)
    
    return None  
