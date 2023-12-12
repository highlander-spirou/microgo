import pymongo
from gridfs import GridFS
from bson import ObjectId
client = pymongo.MongoClient("mongodb://accessuser:accesspwd@localhost:27017?authSource=image_records")


try:
    db = client['image_records']
    collection = db.get_collection('fs.files')

    # for i in collection.find({'owner': 'a'}):
        # print(i)
    fs = GridFS(db)
    fs_id = fs.put(b'hello')
    print(type(fs_id))
    # i = fs.get(ObjectId('65789498589d75dfe7692068'))
    # print(i.read())
    # for i in fs.find({'_id': ObjectId('65789498589d75dfe7692068')}):
    #     print(i.read())
    # out = fs.get('65789498589d75dfe7692069')
    # print(out)

except Exception as e:
    print(f"Connection failed: {e}")

finally:
    # Close the connection
    client.close()