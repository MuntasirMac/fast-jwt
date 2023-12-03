from pymongo import MongoClient
# from motor.motor_asyncio import AsyncIOMotorClient


def connect_db():
    client = MongoClient('mongodb://localhost:27017')
    db = client.get_database('fast-jwt')

    return db

def connect_motor():
    
    motor_client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = motor_client.get_database('library_ms')
    return db