import uvicorn
from fastapi import FastAPI
from src.web.rider import router as rider_router  # Import đúng router
from fastapi.middleware.cors import CORSMiddleware

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

# ✅ Đăng ký router để Swagger nhận diện API
app.include_router(rider_router)

if __name__ == "__main__":
    uvicorn.run("rider:app", reload=True, host="0.0.0.0", port=8002)  # Chạy đúng file chính
