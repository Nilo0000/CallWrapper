# Overview

 - Point of the program is to automate a customer service agent using AI.
 - Uses MongoDB database to store content to be used for context by LLM
 - Context can be loaded using website scraping for now
	 - Future additions may include, not limited to **XML, CSV, text files etc**
 - Front-end will be incorporated eventually
 - Uses OOP to sequentially load context for the LLM to read from, may find some better ways for clean up later
 - Uses embedding to find reasonable content to pull from into temporary_context for LLM to use

A big focus for this is to **reduce costs**, using more computation power by the local machine to parse information, organize information and then mainly use OpenAI and Twilio for *1. AI capabilities, 2. Output 3.  Computation*. Plan is to reduce costs by nearly 50-80% (absolute maximum 50c per call).

**APIs Used**
 - MongoDB Atlas database 
 - OpenAI Response
 - OpenAI Runtime API **Not implemented yet but planned**
 - Twilio Voice **Not implemented yet but planned**

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

## Future Plans (as of 2025-05-12)
 - Add OpenAI's runtime API to chunk up voices, only input should be used and output will be simple TTS by perhaps twilio or something else
	 - More information: https://platform.openai.com/docs/guides/realtime-vad
 - Incorporate calling and whatnot (2nd front-end sort of)
 - Create a website for uploading content, user ended

 Planning on then using AWS to host service for fast computation, perhaps Lambda or something. 