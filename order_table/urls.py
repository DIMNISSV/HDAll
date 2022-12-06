from django.urls import path
from . import views

urlpatterns = [
    path('', views.AddOrder.as_view(), name='order'),
    path('<int:pk>/', views.order_complete, name='order_complete')
]
