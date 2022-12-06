from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.SearchView.as_view(), name='general_search')
]
