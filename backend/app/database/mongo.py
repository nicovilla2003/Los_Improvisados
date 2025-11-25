from pymongo import MongoClient
from os import getenv

MONGO_URI = getenv("MONGO_URI")
MONGO_DB = getenv("MONGO_DB")

client = MongoClient(MONGO_URI)
mongo_db = client[MONGO_DB]
