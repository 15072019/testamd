import uvicorn
from fastapi import FastAPI, HTTPException
from kafka import KafkaProducer, KafkaConsumer
from src.web.rider import router as rider_router
import json
import threading
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
app.include_router(rider_router,tags=["Rider"])
def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def json_deserializer(data):
    return json.loads(data.decode('utf-8'))

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    api_version=(0, 11, 5),
    value_serializer=json_serializer
)

# Lưu trữ dữ liệu ride_matches từ Kafka
ride_matches_cache = []

def consume_ride_matches():
    """
    Lắng nghe Kafka topic 'ride_matches' để lấy user_id và rider_id.
    """
    global ride_matches_cache
    consumer = KafkaConsumer(
        'ride_matches',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        value_deserializer=json_deserializer
    )

    for msg in consumer:
        ride_matches_cache.append(msg.value)
        print(f"📥 Rider received match: {msg.value}")

# Chạy consumer trong background thread
thread = threading.Thread(target=consume_ride_matches, daemon=True)
thread.start()

@app.get("/rider/consume_bookings")
def consume_bookings():
    """
    Lấy danh sách ride_matches từ cache (tối đa 5 chuyến gần nhất).
    """
    if not ride_matches_cache:
        raise HTTPException(status_code=404, detail="No bookings found")
    
    print(f"📄 Returning ride matches: {ride_matches_cache[-5:]}")
    return {"messages": ride_matches_cache[-5:]}

@app.post("/rider/accept_ride")
def accept_ride():
    """
    Nhận chuyến đi gần nhất từ cache và gửi trạng thái "Accepted" vào Kafka.
    """
    if not ride_matches_cache:
        raise HTTPException(status_code=400, detail="No rides available")

    latest_match = ride_matches_cache.pop(0)
    print(f"✅ Processing ride: {latest_match}")

    user_id = latest_match.get("user_id")
    rider_id = latest_match.get("rider_id")

    if not user_id or not rider_id:
        print("❌ Invalid ride data received")
        raise HTTPException(status_code=400, detail="Invalid ride data")

    ride_status = {
        "user_id": user_id,
        "rider_id": rider_id,
        "status": "Accepted"
    }

    producer.send('ride_status_updates', ride_status)
    print(f"🚀 Ride accepted and status updated: {ride_status}")

    return {"status": "Ride accepted", "user_id": user_id, "rider_id": rider_id}

if __name__ == "__main__":
    uvicorn.run("rider:app", reload=True, host="0.0.0.0", port=8002)