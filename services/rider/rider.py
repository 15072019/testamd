import uvicorn
from fastapi import FastAPI
from src.web.rider import router as rider_router  
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaProducer, KafkaConsumer
import json

origins = [
    "*",
    "http://localhost:8002",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rider_router)

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
    'ride_bookings',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=json_deserializer
)

@app.get("/rider/consume_bookings")
def consume_bookings():
    messages = [msg.value for msg in consumer]
    return {"messages": messages}

@app.post("/rider/update_status")
def update_status(status: str):
    producer.send('ride_status_updates', {"status": status})
    return {"status": "Ride status updated"}


if __name__ == "__main__":
    uvicorn.run("rider:app", reload=True, host="0.0.0.0", port=8002)  
