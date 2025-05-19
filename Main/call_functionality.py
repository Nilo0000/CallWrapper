
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
VOICE = 'alloy'

# Voice parameters, for the settings for OpenAi and Twilio and others


# When creating a call
@app.api_route("/incoming-call", methods=["GET", "POST"]) # HTTP Request routing
async def incoming_call(request : Request):
    print("Incoming call recieved")

    ######### Initalization #########
    # Create a TwiML response bracket, so creating the XML stuff is a lot easier
    response = VoiceResponse()
    response.say("Connecting to agent, please wait")
    response.pause(length=0.5)
    response.say("Hello! How can I help you today?")

    test_object = conversation(1)
    string_of = test_object.send_call("What are your lighting services?")
    response.say(string_of)

    ######### Connecting to Websocket for streaming #########
    #host = request.url.hostname # Gets the domain for websocket set up
    #connect = Connect() # Connect to twilio for media stream
    #connect.stream(url=f'wss://{host}/media-stream') #Connect to media stream for communication
    #response.append(connect)
    
    del test_object

    return HTMLResponse(content=str(response), media_type="application/xml") # Returns the XML format data




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)