import random

# Distance matrix representing the distance (in km) between users and riders
DISTANCE_MATRIX = [
    [8, 5, 6, 2, 7],  # User_1 -> Riders
    [3, 9, 4, 6, 1],  # User_2 -> Riders
    [5, 2, 8, 7, 4],  # User_3 -> Riders
    [6, 10, 3, 1, 9], # User_4 -> Riders
    [7, 4, 2, 9, 5]   # User_5 -> Riders
]

def get_distance(user_id: int, rider_id: int) -> int:
    if user_id < 1 or user_id > len(DISTANCE_MATRIX):
        return None  

    if rider_id < 1 or rider_id > len(DISTANCE_MATRIX[0]):
        return None 
    
    # Retrieve and return the distance from the matrix
    return DISTANCE_MATRIX[user_id - 1][rider_id - 1]

def get_nearest_rider(user_id: int) -> int:
    if user_id < 1 or user_id > len(DISTANCE_MATRIX):
        return None  

    # Convert user_id to the correct index (array index starts from 0)
    user_index = user_id - 1
    distances = DISTANCE_MATRIX[user_index]

    # Find the minimum distance value 
    min_distance = min(distances)

    # Identify all riders that have the same minimum distance
    nearest_riders = []
    for i, d in enumerate(distances):
        if d == min_distance:
            nearest_riders.append(i + 1)  # Rider ID starts from 1, so add 1

    #riders have the same minimum distance, pick random
    if nearest_riders:
        chosen_rider = random.choice(nearest_riders)
        return chosen_rider
    else:
        return None 
