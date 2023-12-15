from PIL import Image
import pymongo
from gridfs import GridFS
from bson import ObjectId

client = pymongo.MongoClient("mongodb://accessuser:accesspwd@localhost:27017?authSource=image_records")

try:
    db = client['image_records']
    fs = GridFS(db)

    f = fs.get(ObjectId('657b28141818edd87e28ddea'))
    print(f)
    # for i in fs.find({}):
    #     print(i._id)

except Exception as e:
    print(f"Connection failed: {e}")

finally:
    # Close the connection
    client.close()
