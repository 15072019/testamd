import uvicorn
from fastapi import FastAPI
from src.web.booking import router as booking_router  # Import module booking
from fastapi.middleware.cors import CORSMiddleware
import json
from kafka import KafkaConsumer, KafkaProducer



origins = [
    "http://localhost:8003",
]

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

consumer = KafkaConsumer(
    'ride_matches',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=json_deserializer
)

@app.get("/booking/consume_matches")
def consume_matches():
    messages = [msg.value for msg in consumer]
    return {"messages": messages}

@app.post("/booking/create_booking")
def create_booking(booking_data: dict):
    producer.send('ride_bookings', booking_data)
    return {"status": "Booking created"}

if __name__ == "__main__":
    uvicorn.run("booking:app", reload=True, host="0.0.0.0", port=8003)
