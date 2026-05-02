import asyncio
import json
import signal
import websockets

clients = set()

async def safe_send(client, message):
    try:
        await client.send(message)
        return True
    except Exception:
        return False

async def handler(websocket):
    clients.add(websocket)
    print("Client connected:", len(clients))

    try:
        async for message in websocket:
            preview = message[:120] if isinstance(message, str) else str(message)[:120]
            print("Broadcast:", preview)

            dead = []
            # Send to every other connected client. Speaker does not need echo.
            for client in list(clients):
                if client is websocket:
                    continue
                ok = await safe_send(client, message)
                if not ok:
                    dead.append(client)

            for client in dead:
                clients.discard(client)

    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        print("Client error:", repr(e))
    finally:
        clients.discard(websocket)
        print("Client disconnected:", len(clients))

async def main():
    stop = asyncio.Future()

    def ask_exit(*_):
        if not stop.done():
            stop.set_result(None)

    try:
        signal.signal(signal.SIGTERM, ask_exit)
        signal.signal(signal.SIGINT, ask_exit)
    except Exception:
        pass

    async with websockets.serve(
        handler,
        "0.0.0.0",
        9001,
        ping_interval=20,
        ping_timeout=20,
        max_size=2**20,
    ):
        print("Relay server running on port 9001")
        await stop

if __name__ == "__main__":
    asyncio.run(main())
