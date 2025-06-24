# After each websocket customer prompt, get the transcription
from import_libary import *

async def get_speech_transcription(openai_ws):
    """Get the full transcription of the user's speech segment."""
    transcription_event = {
        "type": "conversation.get_transcription",
        "scope": "last_user_segment"
    }
    await openai_ws.send(json.dumps(transcription_event))
    
    # Wait for the transcription response
    response = await openai_ws.recv()
    response_data = json.loads(response)
    
    if response_data.get('type') == 'conversation.transcription':
        return response_data.get('text', '')
    return ''