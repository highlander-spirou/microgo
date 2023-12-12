"""
A CRD (Create, Read, Delete) system for GridFS
"""
from pymongo import MongoClient
from gridfs import GridFS
from typing import TypeAlias
from dtypes import api_response, internal_response
from bson import ObjectId

file: TypeAlias = bytearray

client = MongoClient("mongodb://accessuser:accesspwd@localhost:27017?authSource=image_records")
db = client['image_records']
fs = GridFS(db)


def create_fs(username: str, f: file, filename:str) -> api_response | internal_response:
    try:
        fs_id = fs.put(f, owner=username, filename=filename)
        return str(fs_id),200
    except Exception as e:
        return {"message": "Error while upload the file"}, 500


def read_fs(fs_id:str) -> file:
    f = fs.get(ObjectId(fs_id))
    content = f.read()
    return content


def delete_fs(fs_id:str) -> None | api_response:
    try:
        fs.delete(ObjectId(fs_id))
    except Exception as e:
        return {'message': f'Cannot delete object {fs_id}'}, 500

