from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.panel_view, name='kodik_panel'),
    path(
        'search/<str:title_orig>/'
        '<str:kinopoisk_id>-<str:imdb_id>-<str:shikimori_id>-<str:mdl_id>-<str:worldart_link>/'
        '<int:order_pk>/',
        views.search, name='kodik_search'),
    path('update/<int:pk>/', views.update, name='kodik_update')
]
