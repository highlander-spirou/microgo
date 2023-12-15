from pymongo import MongoClient
from gridfs import GridFS
from typing import TypeAlias
from werkzeug.datastructures import FileStorage
from libs.file_access import create_fs, read_fs
from dtypes import Error, api_response
from libs.img_process import compress_img


client = MongoClient("mongodb://accessuser:accesspwd@localhost:27017?authSource=image_records")
db = client['image_records']
fs = GridFS(db)


file: TypeAlias = FileStorage
def upload_func(username: str, f: file) -> api_response:
    # 1. Upload base img to database
    fs_id = create_fs(username, f, f.filename, tag='original')
    if isinstance(fs_id, Error):
        return {'message': 'Error uploading file'}, 500
    
    # 2. Compress the file
    compressed_id = compress_img(fs_id, username)
    if isinstance(compressed_id, Error):
        return {'message': 'Error compressing file'}, 500
    
    return {'message': f'Successfully compress img, id: {compressed_id}'}, 200