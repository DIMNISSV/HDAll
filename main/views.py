from django.shortcuts import render
from django.views.generic.base import TemplateView

from main.mixins import TitleMixin


class MainView(TemplateView, TitleMixin):
    template_name = 'main/index.html'
