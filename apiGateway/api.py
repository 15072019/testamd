from typing import Optional
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
from src.model import user, rider #Init db
from src.data.init import create_tables
from fastapi.middleware.cors import CORSMiddleware

services = {
    "user": "http://localhost:8001",
    "rider": "http://localhost:8002",
    "booking":"http://localhost:8003",
    "ride_matching": "http://localhost:8004"
}
# Allow requests from any origin
origins = [
    "*"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def forward_request(service_url: str, method: str, path: str, body=None, headers=None):
    async with httpx.AsyncClient() as client:
        url = f"{service_url}{path}"
        response = await client.request (method, url, json=body, headers=headers)
        return response

@app.api_route("/gateway/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], tags=["ApiGateway"])
async def gateway(service: str, path: str, request: Request):
    if service not in services:
        raise HTTPException(status_code=404, detail="Service not found")

    service_url = services[service]
    body = await request.json() if request.method in ["POST", "PUT", "PATCH"] else None

    async with httpx.AsyncClient() as client:
        response = await client.request(request.method, f"{service_url}/{path}", json=body, headers=dict(request.headers))

    return JSONResponse(status_code=response.status_code, content=response.json())


if __name__ == "__main__":
    create_tables()
    uvicorn.run("api:app", reload=True, host="0.0.0.0", port=8000)
