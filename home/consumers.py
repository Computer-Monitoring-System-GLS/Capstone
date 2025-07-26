# import json
# import asyncio
# from websockets.asyncio.server import serve
# # from channels.generic.websocket import AsyncWebsocketConsumer
# from .utils import discover_devices

# class NetworkConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.send_network_devices()

#     async def send_network_devices(self):
#         devices = discover_devices()
#         await self.send(text_data=json.dumps({"devices": devices}))

import json
import asyncio
import websockets
from system_info.utils import discover_devices  # Import function to get system info

async def send_network_devices(websocket, path):
    """Handles WebSocket connections and sends device info periodically."""
    while True:
        devices = discover_devices()  # Fetch system info
        await websocket.send(json.dumps({"devices": devices}))  # Send to client
        await asyncio.sleep(5)  # Wait before sending the next update

async def main():
    """Starts the WebSocket server on port 8001."""
    async with websockets.serve(send_network_devices, "0.0.0.0", 8001):
        print("WebSocket Server running on ws://0.0.0.0:8001")
        await asyncio.Future()  # Keep server running

if __name__ == "__main__":
    asyncio.run(main())  # Start server
