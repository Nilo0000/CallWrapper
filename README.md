# Overview

 - Point of the program is to automate a customer service agent using AI.
 - Uses MongoDB database to store content to be used for context by LLM
 - Context can be loaded using website scraping for now
	 - Future additions may include, not limited to **XML, CSV, text files etc**
 - Front-end will be incorporated eventually
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
5. Name the index "vector_index"

Note: The dimensions value (1536) is specific to OpenAI's text-embedding-3-small model. Adjust if using a different model.

# Files

 - **call_gpt.py** 
	 - Object for calling chatgpt LLM and whatnot
	 - Used for loading temporary_context and cosine similarity comparison to find relevant context --> *More information found in the script itself*
 - **embed_page.py**
	 - Uses OpenAI's embedding API to embed whatever is sent
 - **extra_gpt_information.py**
	 - Used to store more information for the LLM to include
 - **import_library.py**
	 - Holds all the imports so you don't have to copy and paste over and over again
 - **update_data_site.py**
	 - Used to add to the MongoDB database
 - **writify. py**
	 - Used to write to a file for test-purposes, not really required

# Features Added
 - Calls are seamless
 - Transcriptions provided for later context retrieval

 - Future plans:
   - Actual context retrieval
   - Create front end, website
   - Admin panel (for adding users and whatnot)
   - Hook up to Virtual Machine for everything (not a very good way but whatever)

**As of 2025-06-25**
Huge break because of school, since the last update on 2025-05-12
