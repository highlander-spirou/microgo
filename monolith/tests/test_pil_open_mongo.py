from PIL import Image
import pymongo
from gridfs import GridFS
from bson import ObjectId
from io import BytesIO

client = pymongo.MongoClient("mongodb://accessuser:accesspwd@localhost:27017?authSource=image_records")

try:
    db = client['image_records']
    fs = GridFS(db)
    # print(db.list_collection_names())
    # metadata = db.get_collection('fs.files')
    # for i in metadata.find({}):
    #     print(i)

    f = fs.get(ObjectId('6579f6ca203f12373933956b'))
    with open('./sth.webp', 'wb+') as o:
        o.write(f.read())


    # f = fs.get(ObjectId('6579ef10401ecccd302d061d'))
    # imgIO = BytesIO(f.read())
    # img = Image.open(imgIO)
    # with BytesIO() as output:
    #     img.save(output, optimize=True, quality=50, format="WEBP")
    #     contents = output.getvalue()

    # fs_id = fs.put(contents, owner='Nhân', filename='haha.webp')
except Exception as e:
    print(f"Connection failed: {e}")

finally:
    # Close the connection
    client.close()
