import motor.motor_asyncio
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

# Database Configurations

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ['MONGODB_URL'], serverSelectionTimeoutMS=5000)

client.get_io_loop = asyncio.get_event_loop

try:
    conn = client.server_info()
    print(f'Connected to MongoDB Server')
except Exception as e:
    print("Unable to connect to the MongoDB server.")
    print(str(e))

database = client.afternoon_prep

#===================  Database Collections ================
question_collections = database.get_collection("questions")
