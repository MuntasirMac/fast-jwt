from pymongo import MongoClient
from decouple import config

mongo_uri = config('mongo_uri')

def connect_db():
    client = MongoClient(mongo_uri)
    db = client.get_database('fast-jwt')

    return db

def connect_motor():
    
    motor_client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = motor_client.get_database('library_ms')
    return db