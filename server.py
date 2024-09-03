import asyncio
import websockets

connected_clients = set()

async def handler(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Envia a mensagem recebida para todos os clientes conectados
            await asyncio.wait([client.send(message) for client in connected_clients])
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # executa indefinidamente

if __name__ == "__main__":
    asyncio.run(main())
