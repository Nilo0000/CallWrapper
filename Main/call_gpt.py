# Imports
from import_libary import *

# Create a conversation object, with conversation context
# When calling chatgpt, include the prompts of the chatgpt, its respective answers as well as the context retrieved from the database
class conversation():
    '''
        Variables to include
        --> id = integer
        --> temporary context = array[] *private maybe
    '''

    #Constructor
    def __init__(self, id_, temporary_context_, first_prompt_):
        self.id = id_
        self.temporary_context = temporary_context_
        self.first_prompt = first_prompt_

    '''
        Methods to include
        --> create_context() method
            --> based on the first prompt, add to context from the database
            --> takes the first prompt, embeds it, uses cosine similarity comparing with 
            --> if similarity found, takes the contents and puts it into **temporary_context** array
        
        --> send_call() method
            --> When twilio sees a question, or given a question, calls this method
            --> Using the question prompt, calls to api and gets an answer based on the **temporary_array** array context
            --> Response is added to the **temporary_array** array
            --> Response is then embedded, and compared and added to temporary_context 
        
        Objects' information is stored in the database to send and retrieve from
        So when you call and retrieve methods, you call and retrieve from the 
        right conversation object. A conversation object's id is created when a twilio call starts.
    '''

temporary_conversation = conversation(100, ["Bob", "Dylan", 1])
print(temporary_conversation.temporary_context)
del temporary_conversation