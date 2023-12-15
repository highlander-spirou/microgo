"""
A CRD (Create, Read, Delete) system for GridFS
"""
from pymongo import MongoClient
from gridfs import GridFS
from dtypes import api_response, Error
from bson import ObjectId
from werkzeug.datastructures import FileStorage

client = MongoClient("mongodb://accessuser:accesspwd@localhost:27017?authSource=image_records")
db = client['image_records']
fs = GridFS(db)


def create_fs(username: str, f: bytes | FileStorage, filename:str, **kwargs):
    try:
        fs_id = fs.put(f, owner=username, filename=filename, **kwargs)
        return str(fs_id)
    except Exception as e:
        print(str(e))
        return Error()


def read_fs(fs_id:str):
    """
    Returns filename and bytes array of a gridfs
    """
    try:
        f = fs.get(ObjectId(fs_id))
        return f.filename, f.read()
    except Exception as e:
        print(str(e))
        return Error()


def delete_fs(fs_id:str) -> None | api_response:
    try:
        fs.delete(ObjectId(fs_id))
    except Exception as e:
        return {'message': f'Cannot delete object {fs_id}'}, 500


def retrieve_file_metadata(fs_id):
    """
    Meta data cannot be access through gridfs Object,
    but through physical `fs.files` collection in MongoDB
    """
    fs_files = db.get_collection('fs.files')
    metadata = fs_files.find_one({"_id": ObjectId(fs_id)})
    return metadata


def filter_fs(by:str, value:str):
    fs_files = db.get_collection('fs.files')
    metadata = fs_files.find({by: value})
    return metadata
