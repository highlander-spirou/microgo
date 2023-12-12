from pymongo import MongoClient
from gridfs import GridFS
from typing import TypeAlias

client = MongoClient("mongodb://accessuser:accesspwd@localhost:27017?authSource=image_records")
db = client['image_records']
fs = GridFS(db)


file: TypeAlias = bytearray
def upload_func(username: str, f: file, filename:str):
    a = fs.put(b"hello world", owner=username, filename=filename)
    print(a)
    return "Upload"