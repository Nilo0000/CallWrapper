
# Imports
from import_libary import *
app = FastAPI() # initialize the fastapi api

# Websocket set up
PORT = int(os.getenv('PORT', 5050))
LOG_EVENT_TYPES = [  # The allowed functions for Realtime API Calling, VAD should be enabled
    'error', 'response.content.done', 'rate_limits.updated',
    'response.done', 'input_audio_buffer.committed',
    'input_audio_buffer.speech_stopped', 'input_audio_buffer.speech_started',
    'session.created', 'session.updated'
]
VOICE = 'alloy'

# Voice parameters, for the settings for OpenAi and Twilio and others


# When creating a call
@app.api_route("/incoming-call", methods=["GET", "POST"]) # HTTP Request routing
async def incoming_call(request : Request):
    
    ######### Initalization #########
    # Create a TwiML response bracket, so creating the XML stuff is a lot easier
    response = VoiceResponse()
    response.say("Connecting to agent, please wait")
    response.pause(length=1)
    response("Hello! How can I help you today?")

    # Create object for data storage
    data_object = conversation(1)

    ######### Connecting to Websocket for streaming #########
    host = request.url.hostname # Gets the domain for websocket set up
    connect = Connect() # Connect to twilio for media stream
    connect.stream(url=f'wss://{host}/media-stream') #Connect to websocket for communication
    response.append(connect)

    # Print for test
    data_object.create_context("Summary: Lighting systems, climate control, smart doorbell, pine smart, automation")
    data_object.

    return HTMLResponse(content=str(response), media_type="application/xml") # Returns the XML format data




