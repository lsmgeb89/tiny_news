"""MongoDB client"""

from pymongo import MongoClient

MONGO_DB_HOST = "localhost"
MONGO_DB_PORT = 27017
DB_NAME = "tiny-news"

CLIENT = MongoClient(MONGO_DB_HOST, MONGO_DB_PORT)

def get_db(database=DB_NAME):
    """Get MongoDB instance"""
    return CLIENT[database]
