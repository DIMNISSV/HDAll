from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.AllView.as_view(), name='all_post'),
    path('all/<int:page>/', views.AllView.as_view(), name='all_post_page'),
    path('add/', views.PostAddView.as_view(), name='post_add'),
    path('<int:pk>/', views.PostDetail.as_view(), name='post_pk'),
    path('<str:slug>/', views.PostDetail.as_view(), name='post_slug'),
    path('<str:slug>/<str:translate>/<int:ep_num>/', views.PostDetail.as_view(), name='post_ep'),
    path('edit/<int:pk>/', views.PostEditView.as_view(), name='post_edit')
]
