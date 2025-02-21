import asyncio
import websockets
import json

connected_clients = set()

async def chat_handler(websocket):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data['type'] == 'message':
                message_data = {
                    'autor': data['autor'],
                    'mensagem': data['mensagem']
                }
                await broadcast_message(json.dumps(message_data))
    except websockets.ConnectionClosed:
        print("Connection closed")
    finally:
        connected_clients.remove(websocket)

async def broadcast_message(message):
    if connected_clients:
        await asyncio.gather(*[client.send(message) for client in connected_clients])

async def main():
    async with websockets.serve(chat_handler, 'localhost', 6789):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())