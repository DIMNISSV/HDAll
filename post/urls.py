from django.urls import path, re_path
from . import views

urlpatterns = [
    path('all/', views.AllView.as_view(), name='all_post'),
    path('add/', views.PostAddView.as_view(), name='post_add'),
    path('<int:pk>/', views.PostDetail.as_view(), name='post_pk'),
    path('<str:slug>/', views.PostDetail.as_view(), name='post_slug'),
    re_path(r'(?P<slug>[^/]+)/(?P<player>[^/]+)/(?P<translate>.+)-(?P<ep_num>[0-9]+)/$',
            views.PostDetail.as_view(), name='post_ep'),
    # ('<str:slug>/<str:player>/<int:video_pk>/<int:ep_num>/', views.PostDetail.as_view(), name='post_ep_our'),
    path('edit/<int:pk>/', views.PostEditView.as_view(), name='post_edit'),
    path('vote/<int:pk>/', views.vote_view, name='post_vote')
]
