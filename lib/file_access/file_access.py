from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId
from werkzeug.datastructures import FileStorage
from dataclasses import dataclass
from errors import Error, Code, ConnectionFailure
from typing import TypedDict
from datetime import datetime

class Metadict(TypedDict):
    id: str
    filename: str
    tag: str
    original: str | None
    uploadDate: str


@dataclass
class FileAccess:
    config: dict

    def __post_init__(self):
        username = self.config.get('ACCESS_USR')
        pwd = self.config.get('ACCESS_PWD')

        mongo_host = self.config.get('MONGO_HOST')
        mongo_port = self.config.get('MONGO_PORT')

        try:
            print('Checking connection to MongoDB ...') 
            client = MongoClient(f'mongodb://{username}:{pwd}@{mongo_host}:{mongo_port}?authSource=admin', serverSelectionTimeoutMS=5000)
            self.db = client['image_records']
            self.fs = GridFS(self.db)
        except ConnectionFailure:
            print('Cannot connect to MongoDB, closing server')
            exit()
        client = MongoClient(f'mongodb://{username}:{pwd}@{mongo_host}:{mongo_port}?authSource=admin')



    def create_fs(self, owner_id: str, f: bytes | FileStorage, filename:str, **kwargs):
        try:
            fs_id = self.fs.put(f, owner_id=owner_id, filename=filename, **kwargs)
            return str(fs_id)
        except Exception as e:
            print(str(e))
            return Error(Code.File_CreateError)


    def read_fs(self, fs_id:str):
        """
        Returns filename and bytes array of a gridfs
        """
        try:
            f = self.fs.get(ObjectId(fs_id))
            return f.filename, f.read()
        except Exception as e:
            print(str(e))
            return Error(Code.File_ReadError)


    def delete_fs(self, fs_id:str):
        try:
            self.fs.delete(ObjectId(fs_id))
        except Exception as e:
            print(str(e))
            return Error(Code.Upload_Error)


    def retrieve_file_metadata(self, fs_id:str):
        """
        Meta data cannot be access through gridfs Object,
        but through physical `fs.files` collection in MongoDB
        """
        fs_files = self.db.get_collection('fs.files')
        metadata = fs_files.find_one({"_id": ObjectId(fs_id)})
        return metadata


    def filter_fs(self, by:str, value:str):
        fs_files = self.db.get_collection('fs.files')
        metadata = fs_files.find({by: value})
        return metadata

    def list_imgs(self, owner_id: str):
        metadict:list[Metadict] = []
        for i in self.filter_fs('owner_id', owner_id):
            format_string = "%H:%M on %d/%m/%Y"
            metadict.append({
                'id': str(i.get('_id')),
                'filename': i.get('filename'),
                'tag': i.get('tag'),
                'uploadDate': datetime.strftime(i.get('uploadDate'), format_string),
                'original': i.get('original')
                })
        return metadict
    
    