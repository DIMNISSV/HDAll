from math import inf

from django.contrib.auth.decorators import permission_required
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import CreateView, ListView

from kodik import utils as kodik_utils
from main.mixins import BaseMixin
from . import models


class AddOrder(CreateView, ListView, BaseMixin):
    template_name = 'order_table/add_order.html'
    model = models.Order
    fields = '__all__'
    title = 'Стол заказов'


def _get_obj(pk, order=None):
    order = order if order else models.Order.objects.get(pk=pk)
    obj = kodik_utils.search(title_orig=order.title_orig, kinopoisk_id=order.kinopoisk_id,
                             imdb_id=order.imdb_id, shikimori_id=order.shikimori_id, mdl_id=order.mdl_id,
                             worldart_link=order.worldart_link)

    return order, obj


def order_confirm(request, pk=None):
    obj = None
    if request.GET:
        obj = models.Order(**request.GET.dict())
    order, obj = _get_obj(pk, obj)
    return render(request, 'post/preview.html', {'order': order, 'object': obj, 'params': request.GET.urlencode()})


@permission_required('post.add_post')
def order_complete(request, pk=None):
    GET = request.GET.dict()
    no_redirect = GET.pop('no_redirect', None)
    obj = None
    if GET and not pk:
        obj = models.Order(**GET)
    order, obj = _get_obj(pk, obj)
    post = kodik_utils.save(obj, order.pk)
    if no_redirect:
        return HttpResponse('')
    return redirect('post_slug', post.slug)
