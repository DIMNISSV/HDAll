from django.shortcuts import redirect
from django.views.generic import CreateView, ListView
from django.contrib.auth.decorators import permission_required
from main.mixins import TitleMixin
from . import models


class AddOrder(CreateView, ListView, TitleMixin):
    template_name = 'order_table/add_order.html'
    model = models.Order
    fields = '__all__'
    title = 'Стол заказов'


@permission_required('post.add_post',)
def order_complete(request, pk):
    obj = models.Order.objects.get(pk=pk)
    return redirect('kodik_search', title_orig=obj.orig_title, kinopoisk_id=obj.kinopoisk_id,
                    imdb_id=obj.imdb_id, shikimori_id=obj.shikimori_id, mdl_id=obj.mdl_id,
                    worldart_link=obj.worldart_link, order_pk=pk)
