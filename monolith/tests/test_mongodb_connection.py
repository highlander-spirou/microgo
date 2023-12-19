import pymongo
from gridfs import GridFS
from bson import ObjectId
client = pymongo.MongoClient("mongodb://accessuser:accesspwd@localhost:27017?authSource=admin")


try:
    db = client['celery_results']

    for col in db.list_collection_names():
        print(col)

    # collection = db.get_collection('system.users')
    # for i in collection.find({}):
    #     print(i)
except Exception as e:
    print(f"Connection failed: {e}")

finally:
    # Close the connection
    client.close()