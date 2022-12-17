from django.shortcuts import render
from django.views.generic.base import TemplateView

from main.mixins import BaseMixin


class MainView(TemplateView, BaseMixin):
    template_name = 'main/index.html'
