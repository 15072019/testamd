import uvicorn
from fastapi import FastAPI
from src.web.user import router as user_router  
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaProducer, KafkaConsumer
import json
origins = [
    "*",
    "http://localhost:8001",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router)

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def json_deserializer(data):
    return json.loads(data.decode('utf-8'))

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    api_version=(0, 11, 5),
    value_serializer=json_serializer
)

consumer = KafkaConsumer(
    'ride_status_updates',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=json_deserializer
)

@app.post("/user/request_ride")
def request_ride(user_id: int):
    producer.send('ride_requests', {"user_id": user_id})
    return {"message": "Ride request sent"}

@app.get("/user/ride_status")
def ride_status():
    messages = [msg.value for msg in consumer]
    return {"statuses": messages}

if __name__ == "__main__":
    uvicorn.run("user:app", reload=True, host="0.0.0.0", port=8001)
