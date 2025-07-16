# Overview

 - Point of the program is to automate a customer service agent using AI.
 - Uses MongoDB database to store content to be used for context by LLM
 - Context is inputted by clients through a website (PDF or web scraper)
	 - Future additions may include, not limited to **XML, CSV, text files etc**
 - Front-end incorporated and connected to MongoDB
 - Uses embedding to find reasonable content to pull from into temporary_context for LLM to use

A big focus for this is to **reduce costs**, using more computation power by the local machine to parse information, organize information and then mainly use OpenAI and Twilio for *1. AI capabilities, 2. Output 3.  Computation*. Plan is to reduce costs by nearly 50-80% (absolute maximum 50c per call).

**APIs Used**
 - MongoDB Atlas database 
 - OpenAI Response
 - OpenAI Runtime API 
 - Twilio Voice

# Setup

## MongoDB Vector Search Setup
To enable fast vector similarity search, you need to create a vector search index in MongoDB Atlas:

1. Go to MongoDB Atlas dashboard
2. Select your database and collection
3. Go to the "Search" tab
4. Create a new search index with the following JSON configuration:
```json
{
  "mappings": {
    "dynamic": true,
    "fields": {
      "embedding": {
        "dimensions": 1536,
        "similarity": "cosine",
        "type": "knnVector"
      }
    }
  }
}
```
5. Name the index whatever it is named

Note: The dimensions value (1536) is specific to OpenAI's text-embedding-3-small model. Adjust if using a different model.

# Files

 - **call_gpt.py** 
	 - Object for calling chatgpt LLM and whatnot
	 - Used for loading temporary_context and cosine similarity comparison to find relevant context --> *More information found in the script itself*
 - **embed_page.py**
	 - Uses OpenAI's embedding API to embed whatever is sent
 - **import_library.py**
	 - Holds all the imports so you don't have to copy and paste over and over again
- **call_functionality.py**
	 - Does all the work with twilio, openai and calls the other functions for proper context retrieval

# Features Added
 - Calls are seamless
 - Transcriptions used to get relevant context using mongodb vector search

**As of 2025-06-25**
 - This is the state as of 2025-07-16
 - **Not planning on any more updates**

Front-end GITHUB is also available on my github (should be public) - Uses django as the main web framework.

**Requirements**
 - Requirements are provided in the requirements.txt file


***You need a "container.env" for environment variables. Format as follows:***
hostPORT= <localhost port here> --> Based on your endpoint/ngrok tunnel (THIS IS IF YOU'RE RUNNING ON A VIRTUAL MACHINE OR SERVER OR SOMETHING)
mongo_login= <api key here>
openai_key= <openai key here>

Probably need to use the loadenv library unless you're creating system environment variables (globally)