from django.urls import path
from . import views

urlpatterns = [
    path('', views.AddOrder.as_view(), name='order'),
    path('confirm/', views.order_confirm, name='order_confirm_params'),
    path('confirm/<int:pk>/', views.order_confirm, name='order_confirm'),
    path('complete/', views.order_complete, name='order_complete_params'),
    path('complete/<int:pk>/', views.order_complete, name='order_complete')
]
