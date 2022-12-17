from django.contrib.auth.decorators import permission_required
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


def _get_obj(pk):
    order = models.Order.objects.get(pk=pk)
    obj = kodik_utils.search(title_orig=order.orig_title, kinopoisk_id=order.kinopoisk_id,
                             imdb_id=order.imdb_id, shikimori_id=order.shikimori_id, mdl_id=order.mdl_id,
                             worldart_link=order.worldart_link, order_pk=pk)
    return order, obj


def order_confirm(request, pk):
    order, obj = _get_obj(pk)
    return render(request, 'post/preview.html', {'order': order, 'object': obj})


@permission_required('post.add_post')
def order_complete(request, pk):
    order, obj = _get_obj(pk)
    post = kodik_utils.save(obj, order.pk)
    return redirect('post_slug', post.slug)
