from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import json
import os

from app.database.redis import redis_client
from app.database.clickhouse import ch_client

from app.database.redis import redis_client
from app.database.clickhouse import ch_client
from app.services.ingestor import start_ingestors
from app.services.calculator import fragility_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up Market Fragility Radar v2.0...")
    
    # Start Background Tasks
    asyncio.create_task(start_ingestors())
    asyncio.create_task(fragility_engine.start())
    
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(title="Market Fragility Radar v2.0 API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import dashboard

app.include_router(dashboard.router)

@app.get("/health")
async def health_check():
    redis_status = await redis_client.ping()
    ch_status = ch_client.ping()
    return {
        "status": "healthy",
        "redis": "connected" if redis_status else "error",
        "clickhouse": "connected" if ch_status else "error"
    }

# Legacy WS endpoint at root, can keep or remove. 
# We moved main logic to router, but let's keep a simple echo here or redirect.
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept() # Simple Accept

    try:
        while True:
            # In a real scenario, we would subscribe to Redis channels here
            # For now, just send a heartbeat
            await websocket.send_json({"type": "heartbeat", "status": "connected"})
            await asyncio.sleep(5)
    except Exception as e:
        print(f"WebSocket error: {e}")
