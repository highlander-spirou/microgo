from PIL import Image
import pymongo
from gridfs import GridFS
from bson import ObjectId
from io import BytesIO
import base64

client = pymongo.MongoClient("mongodb://accessuser:accesspwd@localhost:27017?authSource=image_records")
db = client['image_records']
fs = GridFS(db)
f = fs.get(ObjectId('65789498589d75dfe7692068'))
ima_IO = BytesIO(base64.b64decode(f.read()))
img = Image.open(ima_IO)
print(img)