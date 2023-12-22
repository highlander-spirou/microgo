from celery import Celery
from PIL import Image
from time import sleep
from io import BytesIO
from errors import Error
from file_access import FileAccess
from config import config

BROKER_URL = 'amqp://accessuser:accesspwd@localhost:5672/first-vhost'
BACKEND_URL = 'mongodb://root:secret@localhost:27017?authSource=admin'

file_access = FileAccess(config)
task_consumer = Celery('task_consumer', broker=BROKER_URL, backend=BACKEND_URL)


def compress_img(fs_id: str, owner_id:str):
    # read original image from database
    read_result = file_access.read_fs(fs_id)
    if isinstance(read_result, Error):
        return read_result
    
    fs_name, fs_content = read_result
    imgIO = BytesIO(fs_content)
    img = Image.open(imgIO)

    # Mimic a very long task
    sleep(30)

    # Compress image and save to memory as bytes
    with BytesIO() as compressed_img:
        img.save(compressed_img, optimize=True, quality=15, format="WEBP")
        compressed_img_bytes = compressed_img.getvalue()

    # Save the bytes to database
    compressed_id = file_access.create_fs(owner_id, compressed_img_bytes, filename=fs_name, tag='compressed', original=fs_id)
    return compressed_id

@task_consumer.task(name='img_process')
def img_process(fs_id:str, owner_id:str):
    print(f'Receiving {fs_id}')
    compress_img(fs_id, owner_id)
    print(f'{fs_id} process successfully')
    return fs_id


if __name__ == '__main__':
    args = ['worker', '-Q', 'celery_images', '--loglevel=INFO', '--concurrency=2']
    task_consumer.worker_main(argv=args)