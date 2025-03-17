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


if __name__ == "__main__":
    uvicorn.run("rider:app", reload=True, host="0.0.0.0", port=8002)