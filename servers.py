import asyncio
import websockets
import azure.cognitiveservices.speech as speechsdk
import time, io

async def handle_message(websocket, message):
    # Handle the received message here
    speech_config = speechsdk.SpeechConfig(subscription="YourKey", region="YourRegion")

    print("Starting")

    class MyAudioStream(speechsdk.audio.PullAudioInputStreamCallback):
        def __init__(self, message):
            super().__init__()
            self._file_h = io.BytesIO(message)

        def read(self, buffer: memoryview) -> int:
            # Returns audio data to the caller
            # E.g., return read(config.YYY, buffer, size)
            size = buffer.nbytes
            frames = self._file_h.read(size)
            buffer[:len(frames)] = frames

            return len(frames)

        def close(self):
            # Close and clean up resources
            pass

    # Create an instance of your custom audio input stream
    my_stream = MyAudioStream(message)

    stream = speechsdk.audio.PullAudioInputStream(my_stream)

    # Create an audio configuration based on your custom audio input stream
    audio_config = speechsdk.audio.AudioConfig(stream=stream)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    result = ""

    def setResult(evt):
        nonlocal result
        result += evt.result.text

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt.result.text)))
    speech_recognizer.recognized.connect(lambda evt: setResult(evt)) #print('RECOGNIZED: {}'.format(evt))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    #speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()

    await websocket.send(result)


async def wss_endpoint(websocket, path):
    while True:
        message = await websocket.recv()
        await handle_message(websocket, message)

# Set up the WSS server
start_server = websockets.serve(wss_endpoint, '0.0.0.0', 51000, ssl=None, max_size=None, ping_interval=None, ping_timeout=None)

# Start the event loop
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
