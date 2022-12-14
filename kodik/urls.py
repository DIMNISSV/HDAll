from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.panel_view, name='kodik_panel')
]
