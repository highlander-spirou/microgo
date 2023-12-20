from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
try: 
    client = MongoClient("mongodb://accessuser:accesspwd@localhost:27017?authSource=admin", serverSelectionTimeoutMS=5000)
    db = client['image_records']
    print(db.list_collection_names())
except ConnectionFailure:
    print('Cannot connect to MongoDB ...')
    exit()