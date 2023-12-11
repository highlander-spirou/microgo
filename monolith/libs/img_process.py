from PIL import Image
from time import sleep


def compress_img(filename):
    foo = Image.open("./uploads/" + filename)
    # Mimic a very long task
    sleep(5)
    foo.save(f'./uploads/optimized/{filename}', optimize=True, quality=15)
