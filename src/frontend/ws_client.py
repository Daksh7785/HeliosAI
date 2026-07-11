import asyncio
import websockets
import json

async def connect_to_stream():
    uri = "ws://localhost:8000/ws/stream"
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                data = await websocket.recv()
                payload = json.loads(data)
                # Dispatch to Dash Store / Redis
                print("Received payload:", payload)
    except Exception as e:
        print(f"WebSocket error: {e}")

if __name__ == "__main__":
    asyncio.run(connect_to_stream())
