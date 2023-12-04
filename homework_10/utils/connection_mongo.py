from pymongo import MongoClient
from homework_2_10.settings import MONGO_URL

client = MongoClient(MONGO_URL)
db = client.homework_2_10
