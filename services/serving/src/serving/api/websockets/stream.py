from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from structlog import get_logger
import asyncio

logger = get_logger(__name__)

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("websocket_client_connected", total_clients=len(self.active_connections))

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info("websocket_client_disconnected", total_clients=len(self.active_connections))

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error("websocket_broadcast_error", error=str(e))

manager = ConnectionManager()

@router.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # In a real scenario, the backend pushes data here (via Redis pub/sub)
            # This loop just keeps the connection alive for incoming client messages
            await manager.broadcast({"echo": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
