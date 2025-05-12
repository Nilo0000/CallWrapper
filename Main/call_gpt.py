# Imports
from import_libary import *
# GPT set up
openAI_API_Key = os.getenv("OPENAI_API")
openAI_Client = openai.OpenAI(api_key=openAI_API_Key)

# Cosine similarity function
def cosine_similarity(prompt, element):
    score = dot(prompt, element) / (norm(prompt) * norm(element))
    return score

# Create a conversation object, with conversation context
# When calling chatgpt, include the prompts of the chatgpt, its respective answers as well as the context retrieved from the database
class conversation:
    '''
        Variables to include
        --> id = integer
        --> temporary context = array[] *private maybe
        --> client_phone_num = int, phone number of whoever is calling
    '''
    temporary_context = []

    #Constructor
    def __init__(self, id_, client_phone_num_):
        self.id = id_
        self.client_phone_num = client_phone_num_

    '''
        Methods to include
        --> create_context() method
            --> based on the first prompt, add to context from the database
            --> takes the first prompt, embeds it, uses cosine similarity comparing with 
            --> if similarity found, takes the contents and puts it into **temporary_context** array
            --> Temporary_context will be a list of 2D, [id, Text]
        
        --> send_call() method
            --> When twilio sees a question, or given a question, calls this method
            --> Using the question prompt, calls to api and gets an answer based on the **temporary_array** array context
            --> Response is added to the **temporary_array** array
            --> Response is then embedded, and compared and added to temporary_context 
        
        Objects' information is stored in the database to send and retrieve from
        So when you call and retrieve methods, you call and retrieve from the 
        right conversation object. A conversation object's id is created when a twilio call starts.
    '''

    def create_context(self, prompt):
        #Embeddify prompt
        prompt_embed = embed_content(prompt)
        self.temporary_context.append( [prompt_embed, prompt] ) # Sends a list of the actual embedding, and the actual textual prompt/text
    
    def create_message(self, temporary_context):
        string_of = []

        #Add context to the message string
        for element in temporary_context:
            make_string = {"role" : "system", "content" : element[1]}
            string_of.append(make_string) # Appends to the message string array
        
        return string_of


    def send_call(self, prompt):
        # Gets the new prompt and embeds it and adds again
        self.create_context(prompt)

        '''
            Now use that embedded prompt, loops through **mogodb database**
            Then finds relevant **mongodb database** elements, and returns them (for now)
        '''

        # Pages collection
        got_content = pages_collection.find( {"contents" : {"$exists" : True}} )
        
        for element in got_content:
            score = cosine_similarity(self.temporary_context[0][0], element["embedding"])

            # Looks for reasonability
            if (0.35 < score < 1):
                self.temporary_context.append( [element["embedding"], element["contents"]] ) ############# POSSIBLY SEND ID ##############
        
        ## Now that we have context loaded again, we can start to call chatgpt and get results back
        message = self.create_message(self.temporary_context)

        # Now append the prompt
        message.append( {"role" : "user", "content" : "You are personable, and make jokes here and there, respond as if you're talking like a human"} )
        message.append( {"role" : "user", "content" : "You are a customer service agent, use the previous messages as context for answering all questions"} )
        message.append( {"role" : "user", "content" : "Keep messages to around 50 words"} )

        message.append( {"role" : "user", "content" : prompt} )

        # Finally call them!
        response = openAI_Client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message,
        )

        print(response.choices[0].message.content)

test_obj = conversation(1, 4168341740)
test_obj.send_call("Can you tell me about your lighting system services?")
del test_obj


