from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.UploadView.as_view(), name='upload_video'),
    path('update/<int:pk>/', views.EditView.as_view(), name='update_video'),
    path('embed/<int:pk>/', views.EmbedView.as_view(), name='embed_video')
]
