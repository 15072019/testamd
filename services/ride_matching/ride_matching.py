import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.web.ride_matching import router as ride_matching_router
import json
from kafka import KafkaProducer, KafkaConsumer

origins = ["*"]

app = FastAPI()
app.include_router(ride_matching_router, tags=["Ride matching"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# producer = KafkaProducer(
#     bootstrap_servers="localhost:9092",
#     value_serializer=lambda v: json.dumps(v).encode("utf-8"),
# )

# @app.get("/ride-matching/process/{booking_id}")
# def process_ride_matching(booking_id: int):
#     from src.web.ride_matching import get_ride_distance
#     try:
#         ride_data = get_ride_distance(booking_id)
#          producer.send("ride-matching-topic", ride_data)
#         return {"message": "Ride matching processed", "data": ride_data}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/ride-matching/events")
# def get_ride_matching_events():
#     try:
#          consumer = KafkaConsumer(
#              "ride-matching-topic",
#              bootstrap_servers="localhost:9092",
#              value_deserializer=lambda m: json.loads(m.decode("utf-8")),
#              auto_offset_reset="earliest",
#              enable_auto_commit=True,
#          )

#         events = []
#          for message in consumer:
#              events.append(message.value)
#              if len(events) >= 6:
#                  break

#         return {"events": events}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("services.ride_matching:app", reload=True, host="0.0.0.0", port=8004)
