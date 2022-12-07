from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from . import utils
from order_table import models as order_models


def panel_view(request):
    return render(request, 'kodik/panel.html', context={})


def search(request, **kwargs):
    kwargs = {k: v for k, v in kwargs.items() if v != 'None'}
    order_pk = kwargs.pop('order_pk')
    obj = utils.search(kwargs)
    order_models.Order.objects.get(pk=order_pk).delete()
    if obj:
        obj.save()
        return HttpResponse('Ok')
    else:
        return HttpResponse('Not Found')


def update(request):
    return None