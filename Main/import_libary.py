
# Database imports
import requests
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo import UpdateOne
import os
import openai
#from writify import writify_method


## Call imports
import base64
import asyncio
import websockets
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.websockets import WebSocketDisconnect
from twilio.twiml.voice_response import VoiceResponse, Connect, Say, Stream

# Environment set up
from dotenv import load_dotenv
load_dotenv(dotenv_path="Main/container.env")


# Math
import numpy as np
from numpy import dot
from numpy.linalg import norm


# MongoDB setup
database_login_credentials = os.getenv("mongo_login")
connectClient = MongoClient(database_login_credentials)
mainData = connectClient["main"]
pages_collection = mainData["pages"]
