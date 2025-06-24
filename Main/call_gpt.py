# Imports
from import_libary import *
from extra_gpt_information import string_of
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
    def __init__(self, id_):
        self.id = id_
        self.temporary_context = []  # Move to instance variable
        self.convo_ticker = 0

    def _get_relevant_context(self, prompt):
        # Embeddify prompt
        prompt_embed = embed_content(prompt)
        
        # If we already have 3 elements, remove the oldest one
        if len(self.temporary_context) >= 3:
            self.temporary_context.pop(0)
            
        self.temporary_context.append([prompt_embed, prompt])  # Store prompt and its embedding
        
        # Use MongoDB's $vectorSearch for efficient similarity search
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": prompt_embed,
                    "numCandidates": 100,
                    "limit": 10
                }
            },
            {
                "$match": {
                    "contents": {"$exists": True}
                }
            },
            {
                "$project": {
                    "contents": 1,
                    "embedding": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]
        
        # Get relevant documents using vector search
        search_results = list(pages_collection.aggregate(pipeline))
        
        # Filter and add relevant context, maintaining max 3 elements
        for doc in search_results:
            if 0.5 < doc["score"] < 1:
                if len(self.temporary_context) >= 3:
                    self.temporary_context.pop(0)
                self.temporary_context.append([doc["embedding"], doc["contents"]])

    def create_message(self, temporary_context):
        string_of = []
        #Add context to the message string
        for element in temporary_context:
            make_string = {"role": "system", "content": element[1]}
            string_of.append(make_string)
        return string_of

    def send_call(self, prompt):
        # Automatically get relevant context for this prompt
        self._get_relevant_context(prompt)
        self.convo_ticker += 1

        # Create message with current context
        message = self.create_message(self.temporary_context)

        # Add the standard prompts
        message.append({"role": "user", "content": "You are personable, respond as if you're talking like a human"})
        message.append({"role": "user", "content": "You are a customer service agent, use ONLY the previous messages as context for answering all questions"})
        message.append({"role": "user", "content": "Keep messages to around 50 words"})
        message.append({"role": "user", "content": prompt})

        # Call OpenAI
        response = openAI_Client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message,
        )

        #writify_method(self.temporary_context)
        return response.choices[0].message.content
    
    def write_context(self):
        # Create a string to store all the stuff
        string_of = ""

        # Now append to the string
        for element in self.temporary_context:
            string_of = string_of + element[1]

        return string_of # Now return the string for context to send to realtime_api

# Example usage
#testobj = conversation(1)
#testobj.send_call("Explain your lighting services")
#for a in testobj.temporary_context:
#    print(a[1])
#del testobj