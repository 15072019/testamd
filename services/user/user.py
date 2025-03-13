import uvicorn
from fastapi import FastAPI
from kafka import KafkaProducer
from src.web.user import router as user_router  
import json
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app = FastAPI()
app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    api_version=(0, 11, 5),
    value_serializer=json_serializer
)

@app.post("/user/request_ride")
def request_ride(user_id: int):
    """
    Gửi yêu cầu đặt xe (chứa user_id) lên Kafka topic 'ride_requests'.
    """
    ride_request = {"user_id": user_id}
    producer.send('ride_requests', ride_request)
    return {"message": f"Ride request sent for user {user_id}"}

if __name__ == "__main__":
    uvicorn.run("user:app", reload=True, host="0.0.0.0", port=8001)