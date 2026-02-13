from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from app.database.redis import redis_client
from app.database.clickhouse import ch_client
import json
import logging

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])
logger = logging.getLogger(__name__)

@router.get("/status")
async def get_system_status():
    """
    Returns the current health and status of the radar system.
    """
    return {
        "status": "online",
        "redis": await redis_client.ping(),
        "clickhouse": ch_client.ping()
    }

@router.get("/fragility")
async def get_current_fragility():
    """
    Returns the latest Fragility Index and metrics.
    """
    data = await redis_client.get("fragility_index")
    if not data:
        return {"score": 0, "regime": "GREEN", "message": "System initializing..."}
    return json.loads(data)

@router.get("/history")
async def get_fragility_history(limit: int = 100):
    """
    Returns historical fragility data from ClickHouse.
    """
    # DEMO: Returning mock history if ClickHouse is empty or for speed
    # In prod: ch_client.query("SELECT * FROM fragility_metrics ORDER BY timestamp DESC LIMIT {limit}")
    return {
        "history": []
    }

# WebSocket Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Subscribe to Redis channel and forward to WS
        pubsub = redis_client.redis.pubsub()
        await pubsub.subscribe("fragility_updates", "trades:BTCUSDT")
        
        async for message in pubsub.listen():
            if message['type'] == 'message':
                await websocket.send_text(message['data'])
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WS Error: {e}")
        manager.disconnect(websocket)
