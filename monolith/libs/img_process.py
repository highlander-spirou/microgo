from PIL import Image
from time import sleep
from libs.file_access import read_fs, create_fs
from io import BytesIO
from dtypes import Error

def compress_img(fs_id: str, username:str, filename:str| None=None):
    # read original image from database
    read_result = read_fs(fs_id)
    if isinstance(read_result, Error):
        return read_result
    fs_name, fs_content = read_result
    imgIO = BytesIO(fs_content)
    img = Image.open(imgIO)

    # Mimic a very long task
    sleep(300)

    # Compress image and save to memory as bytes
    with BytesIO() as compressed_img:
        img.save(compressed_img, optimize=True, quality=15, format="WEBP")
        compressed_img_bytes = compressed_img.getvalue()

    # Save the bytes to database
    if filename is not None:
        compressed_id = create_fs(username, compressed_img_bytes, filename=filename, tag='compressed', original=fs_id)
    else:
        compressed_id = create_fs(username, compressed_img_bytes, filename=fs_name, tag='compressed', original=fs_id)
    return compressed_id
