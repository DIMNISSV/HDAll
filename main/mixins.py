from django.utils.datetime_safe import datetime
from django.views.generic.base import ContextMixin
from account import models as account_models


class UserParamsMixin:
    def get_paginate_by(self, *args):
        paginate_by = super().get_paginate_by(*args)
        paginate_by = paginate_by if paginate_by else self.request.user.page_size \
            if self.request.user.is_authenticated else 12
        return paginate_by


class BaseMixin(ContextMixin):
    title = 'JustWatch'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.title:
            context["page_title"] = self.title

        context['back_url'] = self.request.GET.get('back')

        if not self.request.user.is_anonymous and not (
                self.request.user.subscribe or self.request.user.subscribe_to
                or (self.request.user.subscribe_to and self.request.user.subscribe_to < datetime.now())):
            subscribe = account_models.Subscribe.objects.get_or_create(price=0)
            if subscribe[1]:
                subscribe.title = 'Бесплатная'
                subscribe.save()
            self.request.user.subscribe = subscribe[0]
            self.request.user.save()
        return context
