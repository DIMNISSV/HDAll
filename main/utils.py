from io import BytesIO
from pathlib import Path
from PIL import Image


def convert_img(img, old_path):
    with open(img.path, 'wb') as f:
        Image.open(old_path).save(f, format='WEBP', quality=90)
    Path(old_path).unlink()

