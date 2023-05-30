import asyncio
import websockets

uri = "wss://localhost:51000" #local

async def send_messages():
    async with websockets.connect(uri, ssl=None, max_size=None, ping_interval=None, ping_timeout=None) as websocket:
        while True:
            path = input("Enter path to file to send (or 'exit' to quit): ")
            if path == "exit":
                await websocket.close()
                break

            file = open(path, "rb")
            message = file.read()
            await websocket.send(message)
            response = await websocket.recv()
            print("\nReceived response:", response)

# Run the test client
asyncio.get_event_loop().run_until_complete(send_messages())
