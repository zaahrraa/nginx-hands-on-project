#!/usr/bin/env python3
import asyncio
import websockets
import datetime

async def echo(websocket):
    print(f"Client connected!")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            response = f"Server received: {message}. Time: {datetime.datetime.now()}"
            await websocket.send(response)
    except Exception as e:
        print(f"Error: {e}")

async def main():
    async with websockets.serve(echo, "127.0.0.1", 5000):
        print("✅ WebSocket server running on ws://127.0.0.1:5000")
        print("Waiting for connections...")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())