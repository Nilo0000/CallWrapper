# Imports
from embed_page import *
from extra_gpt_information import string_of
from import_libary import *
import os
import openai
from numpy import dot
from numpy.linalg import norm
from pymongo import MongoClient

# GPT set up
openAI_API_Key = os.getenv("openai_key")
openAI_Client = openai.OpenAI(api_key=openAI_API_Key)

# MongoDB setup (add your connection details)
mongo_client = MongoClient(os.getenv("mongo_login_BACKEND"))
database = mongo_client["main"]
pages_collection = database["content"]

# Cosine similarity function (kept for reference, but not needed with MongoDB vector search)
def cosine_similarity(prompt, element):
    score = dot(prompt, element) / (norm(prompt) * norm(element))
    return score

def get_relevant_context(prompt, username):
    """
    Gets relevant context from MongoDB using vector search, filtered by username
    
    Args:
        prompt (str): The user's query/prompt
        username (str): Username to filter results by
    
    Returns:
        str: Concatenated relevant content from search results for the specified user
    """
    try:
        # Embed the prompt
        embedded_prompt = embed_content(prompt)
        
        # Ensure embedding is a list (required for MongoDB vector search)
        if not isinstance(embedded_prompt, list):
            embedded_prompt = embedded_prompt.tolist()

        # MongoDB vector search pipeline with username filtering
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "content_vector_search",  # Make sure this matches your index name
                    "path": "embedding",
                    "queryVector": embedded_prompt,
                    "numCandidates": 15,  # Increased since we're filtering afterward
                    "limit": 2,  # Get more results before filtering
                    "filter": {"Username":username}
                }
            },
            {
                "$project": {
                    "title": 1,
                    "content": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]
        
        # Execute the search
        search_results = list(pages_collection.aggregate(pipeline))
        
        # Process results
        relevant_content = ""
        
        # now loop through the search_results and return the content
        for doc in search_results:
            score = doc.get("score")
            
            # Now if they're relevant enough, get their content
            if score > 0.7:
                content = pages_collection.find_one(
                    {"_id": doc.get("_id")}
                )
                
                # Truncate the content
                relevant_content += content.get("Content")
        
        # Some simple rate limiting
        if len(relevant_content) <= 8000:
            return relevant_content
        else:
            return relevant_content[:7999]
        
    except Exception as e:
        print(f"Error in vector search: {str(e)}")
        return ""