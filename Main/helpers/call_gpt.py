# Imports
from embed_page import *
from extra_gpt_information import string_of
from import_libary import *

# GPT set up
openAI_API_Key = os.getenv("OPENAI_API")
openAI_Client = openai.OpenAI(api_key=openAI_API_Key)

# Cosine similarity function
def cosine_similarity(prompt, element):
    score = dot(prompt, element) / (norm(prompt) * norm(element))
    return score

"""
Possible things to do here
 - Gets send a string from call_functionality.py
 - Does a vector search on the database
 - Gets around 2-3 relevant indexes, truncate the strings, return that
 - String gets added to conversation.item
 - AI uses that context
"""

def get_relevant_context(prompt):
    # Embed the prompt
    embedded_prompt = embed_content(prompt)

    # Use MongoDB's $vectorSearch for efficient similarity search
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": embedded_prompt,
                "numCandidates": 5,
                "limit": 2
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
    truncate_string = " "

    # Filter and add relevant context
    for doc in search_results:
        if 0.7 < doc["score"] < 1:
            truncate_string += doc["contents"]
    
    # Returns it
    print(truncate_string)
    #return truncate_string

print("STARTING, sent roblox")
get_relevant_context("ROBLOX")