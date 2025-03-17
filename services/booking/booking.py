import uvicorn
from fastapi import FastAPI, HTTPException
from kafka import KafkaProducer, KafkaConsumer
from src.web.booking import router as booking_router
import json
from fastapi.middleware.cors import CORSMiddleware
import time

origins = ["*"]

app = FastAPI()
app.include_router(booking_router, tags=["Booking"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("booking:app", reload=True, host="0.0.0.0", port=8003)