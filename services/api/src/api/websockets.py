import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict

logger = logging.getLogger(__name__)

router = APIRouter()

class ConnectionManager:
    """
    Manages WebSocket connections and broadcasts (Doc 33 - WebSocket System).
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Client disconnected. Active connections: {len(self.active_connections)}")

    async def broadcast_telemetry(self, message: Dict):
        """
        Broadcasts live telemetry or forecast updates to all connected dashboard clients.
        """
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Failed to send message to client: {e}")
                self.disconnect(connection)

manager = ConnectionManager()

@router.websocket("/ws/telemetry")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Typically clients just listen, but they could send ping/pong or filters here.
            data = await websocket.receive_text()
            logger.debug(f"Received message from client: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
