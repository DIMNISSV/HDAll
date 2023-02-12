from django.views.generic.base import TemplateView
from post import models as post_models
from main.mixins import BaseMixin


class MainView(TemplateView, BaseMixin):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest'] = post_models.Post.objects.filter()[:5]
        return context
