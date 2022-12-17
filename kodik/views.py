from django.shortcuts import render
from main.mixins import BaseMixin
from django.views.generic.base import TemplateView


class PanelView(TemplateView, BaseMixin):
    template_name = 'kodik/panel.html'
    title = 'Панель управления KODIK'
