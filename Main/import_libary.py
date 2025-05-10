import requests
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo import UpdateOne
import os
import openai
from embed_page import embed_content
from embed_page import textify_embed

# MongoDB setup
database_login_credentials = os.getenv("mongoDB_login")
connectClient = MongoClient(database_login_credentials)
mainData = connectClient["main"]
pages_collection = mainData["pages"]

# GPT set up
openAI_API_Key = os.getenv("openAI_API_Key")
openAI_Client = openai.OpenAI(api_key=openAI_API_Key)