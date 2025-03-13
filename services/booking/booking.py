import uvicorn
from fastapi import FastAPI
from kafka import KafkaProducer, KafkaConsumer
from src.web.booking import router as booking_router
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
app.include_router(booking_router)

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def json_deserializer(data):
    return json.loads(data.decode('utf-8'))

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    api_version=(0, 11, 5),
    value_serializer=json_serializer
)

ride_requests_cache = []

def consume_requests():
    """
    Lắng nghe Kafka topic 'ride_requests' để lấy user_id và lưu vào cache.
    """
    global ride_requests_cache
    consumer = KafkaConsumer(
        'ride_requests',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        value_deserializer=json_deserializer
    )

    for msg in consumer:
        ride_requests_cache.append(msg.value)
        print(f"📥 Booking received ride request: {msg.value}")

thread = threading.Thread(target=consume_requests, daemon=True)
thread.start()

@app.post("/booking/create_booking")
def create_booking():
    """
    Nhận user_id từ cache, tạo booking, gửi tiếp vào Kafka topic 'ride_bookings'.
    """
    if not ride_requests_cache:
        return {"error": "No ride requests available"}

    latest_request = ride_requests_cache.pop(0)  
    user_id = latest_request.get("user_id")

    if not user_id:
        return {"error": "Invalid request data"}

    booking_data = {"user_id": user_id, "booking_status": "confirmed"}
    producer.send('ride_bookings', booking_data)
    print(f"🚀 Booking created and sent to Kafka: {booking_data}")

    return {"status": "Booking created", "user_id": user_id}

@app.post("/booking/send_to_matching")
def send_to_matching():
    """
    Gửi user_id từ booking đến ride_matching để tìm tài xế và tính giá tiền.
    """
    if not ride_requests_cache:
        return {"error": "No ride requests available"}

    latest_request = ride_requests_cache.pop(0) 
    user_id = latest_request.get("user_id")

    if not user_id:
        return {"error": "Invalid request data"}

    ride_matching_data = {"user_id": user_id}
    producer.send('ride_matching_requests', ride_matching_data)
    print(f"🔄 Sent user_id to ride_matching: {ride_matching_data}")

    return {"status": "Sent to ride_matching", "user_id": user_id}

if __name__ == "__main__":
    uvicorn.run("booking:app", reload=True, host="0.0.0.0", port=8003)