
# Imports
from import_libary import *
from call_gpt import conversation
app = FastAPI() # initialize the fastapi api

# GPT set up
openAI_API_Key = os.getenv("OPENAI_API")

'''
    All of these async functions happen in parallel, with websocket requests so calls are streamlined
'''

# Websocket set up
PORT = int(os.getenv('PORT', 5050))
LOG_EVENT_TYPES = [  # The allowed functions for Realtime API Calling, VAD should be enabled
    'error', 'response.content.done', 'rate_limits.updated',
    'response.done', 'input_audio_buffer.committed',
    'input_audio_buffer.speech_stopped', 'input_audio_buffer.speech_started',
    'session.created', 'session.updated'
]
VOICE = 'sage'

# Voice parameters, for the settings for OpenAi and Twilio and others


##################################### INCOMING CALL #######################################
@app.api_route("/incoming-call", methods=["GET", "POST"]) # HTTP Request routing
async def incoming_call(request : Request):
    print("Incoming call recieved")

    ######### Initalization #########
    # Create a TwiML response bracket, so creating the XML stuff is a lot easier
    response = VoiceResponse()
    response.say("Connected")

    ######### Connecting to Websocket for streaming #########
    host = request.url.hostname # Gets the domain for websocket set up
    connect = Connect() # Connect to twilio for media stream
    connect.stream(url=f'wss://{host}/media-stream') #Connect to media stream for communication
    response.append(connect)

    return HTMLResponse(content=str(response), media_type="application/xml") # Returns the XML format data

######################### MEDIA STREAM ######################################
@app.websocket("/media-stream")
async def handle_media_stream(ws: WebSocket):
    print("Client Connected")
    await ws.accept()

    try:
        async with websockets.connect(
            'wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17',
            additional_headers={
                "Authorization": f"Bearer {openAI_API_Key}",
                "OpenAI-Beta": "realtime=v1"
            },
            ping_interval=100,
            ping_timeout=100
        ) as opws:
            await send_session_update(opws)

            # Create an event to signal when to stop
            stop_event = asyncio.Event()

            async def rec_from_twilio():
                try:
                    async for message in ws.iter_text():
                        if stop_event.is_set():
                            break
                            
                        data = json.loads(message)
                        if data['event'] == 'media':
                            try:
                                await opws.send(json.dumps({
                                    "type": "input_audio",
                                    "data": data['media']['payload'],
                                }))

                            except websockets.exceptions.ConnectionClosed as e:
                                print(f"OpenAI connection closed during send — Code: {e.code}, Reason: {e.reason}")
                                stop_event.set()
                                break
                except Exception as e:
                    print(f"Twilio receiver error: {str(e)}")
                    stop_event.set()

            async def send_to_twilio():
                try:
                    async for message in opws:
                        if stop_event.is_set():
                            break
                            
                        data = json.loads(message)
                        if data["type"] == "input_audio_buffer.speech_started":
                            print("Speech Started")
                        elif data["type"] == "input_audio_buffer.speech_stopped":
                            print("Speech Stopped")
                        elif data["type"] == "output_audio":
                            try:
                                await ws.send_text(json.dumps({
                                    "event": "media",
                                    "media": {
                                        "payload": data["data"],
                                        "encoding": "ulaw",
                                        "sampleRate": 8000
                                    }
                                }))
                            except websockets.exceptions.ConnectionClosed as e:
                                print(f"Twilio WebSocket closed during send — Code: {e.code}, Reason: {e.reason}")
                                stop_event.set()
                                break
                except Exception as e:
                    print(f"OpenAI receiver error: {str(e)}")
                    stop_event.set()

            # Run both tasks and wait for completion
            twilio_task = asyncio.create_task(rec_from_twilio())
            openai_task = asyncio.create_task(send_to_twilio())

            # Wait for either task to complete (which will set the stop_event)
            done, pending = await asyncio.wait(
                [twilio_task, openai_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            # Cleanup
            stop_event.set()
            for task in pending:
                task.cancel()
            try:
                await asyncio.gather(*pending, return_exceptions=True)
            except:
                pass

    except Exception as e:
        print(f"WebSocket connection error: {str(e)}")
    finally:
        print("Media stream connection closed")

############################### UPDATE REALTIME API SETTINGS ################################
async def send_session_update(openai_ws):
    """Send session update to OpenAI WebSocket."""
    session_update = {
        "type": "session.update",
        "session": {
            "turn_detection": {"type": "server_vad"},
            "input_audio_format": "g711_ulaw",
            "turn_detection.create_response":"false",
            "turn_detection.interrupt_response":"false",
            "output_audio_format": "g711_ulaw",
            "voice": VOICE,
            "instructions": "You are a customer service agent, talk humanly and politely",
            "modalities": ["text", "audio"],
            "temperature": 0.8,
        }
    }
    print('Sending session update:', json.dumps(session_update))
    await openai_ws.send(json.dumps(session_update))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)