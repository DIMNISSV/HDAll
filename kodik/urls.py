from django.urls import path
from . import views

urlpatterns = [
    path('', views.PanelView.as_view(), name='kodik_panel')
]
