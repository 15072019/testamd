import uvicorn
from fastapi import FastAPI
from src.web.ride_matching import router as ride_matching_router  # Import module booking
from fastapi.middleware.cors import CORSMiddleware
import json
from kafka import KafkaProducer, KafkaConsumer
origins = [
    "http://localhost:8004",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ride_matching_router)

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
    'ride_requests',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=json_deserializer
)

@app.get("/ride_matching/consume_requests")
def consume_requests():
    messages = [msg.value for msg in consumer]
    return {"messages": messages}

@app.post("/ride_matching/match_rider")
def match_rider(match_data: dict):
    producer.send('ride_matches', match_data)
    return {"status": "Ride match sent"}

if __name__ == "__main__":
    uvicorn.run("ride_matching:app", reload=True, host="0.0.0.0", port=8004)
