import pika, json
from typing import TypeAlias
from gridfs import GridFS
from pika.channel import Channel


file: TypeAlias = any
grid_fs: TypeAlias = GridFS
access: TypeAlias = dict
pika_channel: TypeAlias = Channel

def upload_video(f:file, fs: grid_fs, channel:pika_channel, access: access):
    """
    Upload a video to mongodb database, and enqueue a signal
    """
    # Upload the file
    try:
        fid = fs.put(f)
    except Exception as e:
        return "Error uploading the video", 500
    
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access['username']
    }

    # Enqueue the file
    try:
        channel.basic_publish(
            exchange="", # Exchange name
            routing_key="video", # Queue name
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as e:
        # Delete the video if enqueue fails to avoid stale videos
        fs.delete(fid)
        return "Internal server error", 500
