from pprint import pp

from django.views.generic.base import TemplateView

from main.mixins import BaseMixin
from . import utils


class PanelView(TemplateView, BaseMixin):
    template_name = 'kodik/panel.html'
    title = 'Панель управления KODIK'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all'] = utils.full_list()
        return context
