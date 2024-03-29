import re
from pathlib import Path
from threading import Thread

from PIL import Image
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from slugify import slugify

from kodik import utils as kodik_utils

regex = re.compile(r'^(\d{4}|\d{4}-\d{4})$')


def validate_year(value):
    if not regex.fullmatch(value):
        raise ValidationError(gettext_lazy(f'{value} is not in year(s) format.'))


def gen_slug(obj, num=0):
    slug = slugify(obj.title_orig, only_ascii=True)
    slug = f'{slug}-{num}' if num > 0 else slug
    if obj.__class__.objects.filter(slug=slug).exists():
        num += 1
        slug = gen_slug(obj, num)
    return slug


def get_kodik_list(obj):
    cache_name = f'kodik_list_{obj.pk}'
    kodik_list = cache.get(cache_name)
    if not kodik_list:
        Thread(target=kodik_utils.update, args=(obj,)).start()
        kodik_list = kodik_utils.get_episode_list(obj)
        cache.set(cache_name, kodik_list)
    return kodik_list


def get_video_list(obj, model):
    return {i.ep_num: i for i in model.objects.filter(to_post_id=obj.pk)}


def convert_img(img, old_path):
    with open(img.path, 'wb') as f:
        Image.open(old_path).save(f, format='WEBP', quality=90)

    old_path = Path(old_path)
    if old_path.exists():
        old_path.unlink()
