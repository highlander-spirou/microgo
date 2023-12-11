import json
from flask import Flask, request
from flask_pymongo import PyMongo
from gridfs import GridFS
import pika
from config import config
from libs import login, validate_user, upload_video

app = Flask(__name__)
app.config["MONGO_URI"] = config.get('MONGO_URI')

mongo_video = PyMongo(app, uri="mongodb://host.minikube.internal:27017/videos")
mongo_mp3 = PyMongo(app, uri="mongodb://host.minikube.internal:27017/mp3s")

fs_videos = GridFS(mongo_video.db)
fs_mp3s = GridFS(mongo_mp3.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@app.route('/login', methods=['POST'])
def login_router():
    token, err = login(request)
    if not err:
        return token
    else:
        return err
    

@app.route('/upload', methods=['POST'])
def upload_router():
    access, err = validate_user(request)
    if err:
        return err
    
    access = json.loads(access)
    if access['is_admin']:
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly 1 file required", 400
        for _, f in request.files.items():
            err = upload_video(f, fs_videos, channel, access)

            if err:
                return err

        return "success!", 200
    else:
        return "not authorized", 401
    
@app.route('/download', methods=["POST"])
def download_router():
    pass

if __name__ == '__main__':
    app.run("0.0.0.0")