import uvicorn
from fastapi import FastAPI
from kafka import KafkaProducer
from src.web.user import router as user_router  
import json
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app = FastAPI()
app.include_router(user_router, tags=["User"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("user:app", reload=True, host="0.0.0.0", port=8001)