import uvicorn
from fastapi import FastAPI
from src.web import user
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaConsumer
import json

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

app.include_router(user.router, tags=["User"])

consumer = KafkaConsumer("my_topic", bootstrap_servers='localhost:9092',
                        api_version=(0,11,5),
                        value_deserializer=lambda m: json.loads(m.decode("utf-8")))

@app.get("/consume")
def consume():
    messages = []
    for message in consumer:
        messages.append(message.value)
        if len(messages) >= 3:
            break
    return {"messages": messages}

if __name__ == "__main__":
    uvicorn.run("user:app", reload=True, host="0.0.0.0", port=8001)