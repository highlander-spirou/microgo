import pymongo

client = pymongo.MongoClient("mongodb://accessuser:accesspwd@localhost:27017?authSource=image_records")

try:
    db = client['image_records']
    collections = db.list_collection_names()
    print('Connect successfully')
    print(collections)
except Exception as e:
    print(f"Connection failed: {e}")

finally:
    # Close the connection
    client.close()