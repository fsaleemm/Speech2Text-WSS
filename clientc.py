import asyncio
import websockets
from pydub import AudioSegment
from pydub.utils import make_chunks

uri = "wss://localhost:51000" #local

async def send_messages():
    async with websockets.connect(uri, ssl=None, max_size=None, ping_interval=None, ping_timeout=None) as websocket:
        while True:
            path = input("Enter path to file to send (or 'exit' to quit): ")
            if path == "exit":
                await websocket.close()
                break

            myaudio = AudioSegment.from_file(path , "wav")
            chunk_length_ms = 200 # pydub calculates in millisec
            chunks = make_chunks(myaudio, chunk_length_ms) 

            #Send to S2T all of the individual chunks

            for i, chunk in enumerate(chunks):
                await websocket.send(chunk.raw_data)
                response = await websocket.recv()
                print("Received response:", response)

# Run the test client
asyncio.get_event_loop().run_until_complete(send_messages())
