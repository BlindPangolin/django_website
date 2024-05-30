from io import BytesIO
from django.core.files import File
from PIL import Image
import subprocess


def make_thumbnail(image):
    img = Image.open(image)
    w, h = img.size
    bbox = [0, 0, w, h]
    if w > h:
        margin = w - h
        bbox[0] = margin//2
        bbox[2] = w - (margin - bbox[0])
    elif h > w:
        margin = h - w
        bbox[1] = margin//2
        bbox[3] = h - (margin - bbox[1])
    img = img.crop(tuple(bbox))
    img = img.resize((500, 500))

    thumb_io = BytesIO()
    img.save(thumb_io, 'PNG')
    thumbnail = File(thumb_io, name=image.name.replace('/original/', '/thumbnail/'))

    return thumbnail


def attach_xmp(image_path, xmp_path):
    subprocess.run(['exiftool', '-v', '-tagsfromfile', f"{xmp_path}", '-all:all', f"{image_path}", '-overwrite_original'])
