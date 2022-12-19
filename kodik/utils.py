from __future__ import annotations

import json
from http.client import HTTPResponse
from pprint import pp
from urllib import parse
from urllib import request as req
from urllib.parse import urlencode

from django.core.files.images import ImageFile
from django.core.files.temp import NamedTemporaryFile
from django.urls import reverse_lazy
from slugify import slugify

from Site import settings
from order_table import models as order_models
from post import models as post_models

search_url = f'https://kodikapi.com/search?token={settings.KODIK_TOKEN}'
list_url = f'https://kodikapi.com/list?token={settings.KODIK_TOKEN}'


def _file_from_url(url: str) -> ImageFile:
    tmp_file = NamedTemporaryFile()
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    r = req.Request(url, headers={'User-Agent': ua})
    content = req.urlopen(r).read()
    tmp_file.write(content)
    tmp_file.flush()
    name = parse.urlparse(url).path.split('/')[-1]
    return ImageFile(tmp_file, name)


def _get_field_data(json_data: dict, json_key: str):
    value = None

    levels = json_key.split('.')
    json_data = json_data.get('results', json_data)
    if isinstance(json_data, list):
        json_data = json_data[0]

    if len(levels) > 1:
        result = json_data
        for level in levels:
            result = result.get(level, None)
            if not result:
                break
        value = result
        if not value: return
    elif not value:
        value = json_data.get(json_key, None)

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
        if item.get('seasons'):
            first_item = next(iter(item['seasons'].items()))[1]
            episode_links = tuple(f'{link}?translations=false' for link in first_item.get('episodes').values())
        else:
            first_item = item.get('link')
            episode_links = (f'{first_item}?translations=false',)
        result[item.get('translation').get('title')] = episode_links
    return result


def _episodes_json(json_data: dict) -> dict:
    data = json_data['results']
    episodes = dict()
    if data:
        episodes: dict = _get__eps_with_translations(data)
    return episodes


def _get_ids_param(post, as_url=True, from_dict=False) -> str | dict:
    if from_dict:
        ids = [(name, post[name]) for name in
               settings.KODIK_ID_FIELDS if name in post and
               post[name]]
    else:
        ids = dict(((i, getattr(post, i)) for i in settings.KODIK_ID_FIELDS))

    if as_url:
        return parse.urlencode({k: v for k, v in ids.items() if v})
    else:
        return ids


def _search(kwargs: dict):
    resp: HTTPResponse = req.urlopen(f'{search_url}&with_material_data=true&{urlencode(kwargs)}')
    json_data = json.load(resp)
    obj = None
    if json_data.get('results'):
        obj = json_to_obj(json_data)
    return obj


def _set_m2m_fields(obj, field, data):
    res = []
    data = (data.get('title', ()),) if isinstance(data, dict) else data if isinstance(data, (list, tuple)) else (data,)
    m2m = getattr(obj, field)

    for title in data:
        slug, title = (title, settings.TYPE_TO_CATEGORY.get(title)) if title in settings.TYPE_TO_CATEGORY \
            else (slugify(title, only_ascii=True), title)
        if hasattr(m2m.model, 'slug'):
            i = m2m.model.objects.get_or_create(slug=slug)[0]
        else:
            i = m2m.model.objects.filter(title=title)
            args = {'title': title}
            args.update({'job': 'team'} if hasattr(m2m.model, 'job') else {})
            i = i[0] if i else m2m.model.objects.create(**args)
        if i.title != title:
            i.title = title
            i.save()
        res.append(i)
        post_models.Post()

    m2m.clear()
    m2m.add(*res)

    return obj


def _validate_fields_data(base_obj, kodik_data, model_cls):
    for k, v in kodik_data.items():
        if k and hasattr(base_obj, k) and v:
            if k == 'poster':
                obj = model_cls()
                data = open(v.file.name, 'rb')
                if base_obj.poster:
                    base_obj.poster.delete()
                base_obj.poster = obj.poster
                base_obj.poster.save(v.name, data, save=False)
            elif k in settings.KODIK_M2M_FIELDS and base_obj.pk:
                _set_m2m_fields(base_obj, k, v)
            else:
                setattr(base_obj, k, v)
    return base_obj


def search(**kwargs):
    kwargs = {k: v for k, v in kwargs.items() if v}
    obj = _search(kwargs)
    return obj


def save(obj, order_pk):
    if obj:
        obj.save()
        if order_pk:
            order_models.Order.objects.get(pk=order_pk).delete()
        return obj
    return


def update(obj):
    resp: HTTPResponse = req.urlopen(f'{search_url}&with_material_data=true&{_get_ids_param(obj)}')
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

    if hasattr(model_cls, 'check_exist') and not base_obj:
        base_obj = model_cls.check_exist(**kodik_data)

    base_obj = _validate_fields_data(base_obj, kodik_data, model_cls)

    return base_obj


def get_episode_list(post) -> dict[str, list]:
    resp: HTTPResponse = req.urlopen(f'{search_url}&{_get_ids_param(post)}&with_episodes=true')
    json_data = json.load(resp)
    episodes = _episodes_json(json_data)
    pp(episodes)
    return episodes


def full_list():
    resp: HTTPResponse = req.urlopen(f'{list_url}&limit=5')
    json_data = json.load(resp)
    res = []
    for obj in json_data['results']:
        id_fields = ('title_orig', 'kinopoisk_id', 'imdb_id', 'mdl_id', 'shikimori_id')
        obj = {key: value for key, value in obj.items() if key in id_fields}
        res.append((obj.get('title_orig'), f'{reverse_lazy("order_confirm_params")}?{urlencode(obj)}'))
    return res
