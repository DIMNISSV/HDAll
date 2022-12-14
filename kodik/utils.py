from __future__ import annotations

import json
from http.client import HTTPResponse
from io import FileIO
from pprint import pp
from urllib import parse
from urllib import request as req
from urllib.parse import urlencode

from django.core.files.images import ImageFile
from django.core.files.temp import NamedTemporaryFile
from django.urls import reverse_lazy

from Site import settings
from order_table import models as order_models

base_url = 'https://kodikapi.com/search?token=a9d0ae164383c3a7cdf19cfceadabb0f'


class KodikVideo:
    def __init__(self, post, s_num: int, ep_num: int, translate: str, link: str) -> None:
        self.to_post = post
        self.s_num: int = s_num
        self.ep_num: int = ep_num
        self.link: str = link
        self.translate: str = translate

    def get_absolute_url(self):
        return reverse_lazy('post_ep',
                            kwargs={'slug': self.to_post.slug, 'ep_num': self.ep_num, 'translate': self.translate})


def _file_from_url(url: str) -> ImageFile:
    tmp_file = NamedTemporaryFile()
    tmp_file.write(req.urlopen(url).read())
    tmp_file.flush()
    name = parse.urlparse(url).path.split('/')[-1]
    content = req.urlretrieve(url)
    return ImageFile(FileIO(content[0], 'rb'), name)


def _get_field_data(json_data: dict, json_key: str):
    value = None
    levels = json_key.split('.')
    json_data = json_data.get('results', json_data)
    if isinstance(json_data, list) and len(json_data) > 1:
        json_data = json_data[0]
    if len(levels) > 1:
        result = json_data
        for level in levels:
            result = result.get(level, None)
            if not result:
                break
        value = result
    elif not value:
        value = json_data.get(json_key, None)
    print(json_key)
    if json_key == 'material_data.poster_url':
        value = _file_from_url(value)

    return value


def _get_season(obj):
    if obj.season:
        return obj.season
    elif obj.season_total:
        return obj.season_total
    else:
        return 1


def _get__eps_with_translations(json_data: dict) -> dict[str, tuple]:
    result = dict()
    for item in json_data:
        first_item = next(iter(item.get('seasons').items()))[1]
        episode_links = tuple(link + '?translations=false' for link in first_item.get('episodes').values())
        result[item.get('translation').get('title')] = episode_links
    return result


def _episodes_json(json_data: dict) -> dict:
    data = json_data['results']
    episodes = dict()
    if data:
        pp(data[0])
        episodes: dict = _get__eps_with_translations(data)
    return episodes


# def _link_json(json_data: dict, ep_num: int, translate: str = None):
#     episodes = _episodes_json(json_data, translate)
#     episode = None
#     if episodes:
#         episode = episodes.get(str(ep_num))
#     return episode


def _get_ids_param(post) -> str:
    ids = {
        'kinopoisk_id': post.kinopoisk_id,
        'imdb_id': post.imdb_id,
        'shikimori_id': post.shikimori_id,
        'wa_link': post.wa_link,
        'mdl_id': post.mdl_id,
        'title': post.title
    }
    return parse.urlencode({k: v for k, v in ids.items() if v})


def _search(kwargs: dict):
    resp: HTTPResponse = req.urlopen(f'{base_url}&with_material_data=true&{urlencode(kwargs)}')
    json_data = json.load(resp)
    obj = None
    if json_data.get('results'):
        obj = json_to_obj(json_data)
    return obj


def search(**kwargs):
    kwargs = {k: v for k, v in kwargs.items() if v}
    order_pk = kwargs.pop('order_pk')
    obj = _search(kwargs)
    if obj:
        obj.save()
        order_models.Order.objects.get(pk=order_pk).delete()
        return obj
    return


def update(obj):
    resp: HTTPResponse = req.urlopen(f'{base_url}&with_material_data=true&{_get_ids_param(obj)}')
    json_data: dict = json.load(resp)
    obj = json_to_obj(json_data, obj)
    obj.save()


def json_to_obj(json_data: dict, base_obj=None):
    imp_path, model_name = settings.KODIK_MODEL.rsplit('.', 1)
    model_cls = getattr(__import__(imp_path, fromlist=model_name), model_name)
    settings.KODIK_FIELDS.update(
        dict(zip(settings.KODIK_ONENAME_FIELDS, settings.KODIK_ONENAME_FIELDS)))
    kodik_data = {model_key: _get_field_data(json_data, json_key) for json_key, model_key in
                  settings.KODIK_FIELDS.items()}
    print(base_obj)
    if hasattr(model_cls, 'check_exist') and not base_obj:
        base_obj = model_cls.check_exist(**kodik_data)
    for k, v in kodik_data.items():
        if hasattr(base_obj, k) and v:
            if k == 'poster':
                obj = model_cls()
                data = open(v.file.name, 'rb')
                if base_obj.poster:
                    base_obj.poster.delete()
                base_obj.poster = obj.poster
                base_obj.poster.save(v.name, data, save=False)
            else:
                setattr(base_obj, k, v)

    return base_obj


def get_episode_list(post) -> dict[str, list]:
    resp: HTTPResponse = req.urlopen(f'{base_url}&{_get_ids_param(post)}&with_episodes=true')
    json_data = json.load(resp)
    episodes = _episodes_json(json_data)
    pp(episodes)
    return episodes
