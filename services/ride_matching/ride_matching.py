import uvicorn
from fastapi import FastAPI, HTTPException
from src.web.ride_matching import router as ride_matching_router
from kafka import KafkaProducer, KafkaConsumer
import threading
import json
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ride_matching_router,tags=["Ride matching"])

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def json_deserializer(data):
    return json.loads(data.decode('utf-8'))

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    api_version=(0, 11, 5),
    value_serializer=json_serializer
)

booking_cache = []

def consume_bookings():
    """
    Lắng nghe Kafka topic 'ride_bookings' để lấy user_id và lưu vào cache.
    """
    global booking_cache
    consumer = KafkaConsumer(
        'ride_bookings',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        value_deserializer=json_deserializer
    )

    for msg in consumer:
        booking_cache.append(msg.value)
        print(f"📥 Ride Matching received booking: {msg.value}")

thread = threading.Thread(target=consume_bookings, daemon=True)
thread.start()

@app.post("/ride_matching/match_rider")
def match_rider():
    """
    Nhận booking từ cache, tìm tài xế, và gửi vào Kafka topic 'ride_matches'.
    """
    if not booking_cache:
        raise HTTPException(status_code=400, detail="No bookings available")

    latest_booking = booking_cache.pop(0)
    user_id = latest_booking.get("user_id")

    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid booking data")

    matched_ride = {
        "user_id": user_id,
        "rider_id": "some_rider_id",
        "ride_details": "some_details"
    }

    producer.send('ride_matches', matched_ride)
    print(f" Ride Matched and sent to Kafka: {matched_ride}")

    return {"status": "Ride matched", "user_id": user_id}

if __name__ == "__main__":
    uvicorn.run("ride_matching:app", reload=True, host="0.0.0.0", port=8004)