from django.urls import path, include

from . import views

urlpatterns = [
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('my_profile/', views.ProfileView.as_view(), name='my_profile'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('my_profile/edit/', views.ProfileEdit.as_view(), name='edit_my_profile'),
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('subscribe/complete/', views.subscribe_complete_view, name='subscribe_complete'),
    path('subscribe/<str:subscribe>/', views.SubscribeView.as_view(), name='pay_subscribe'),
    path('subscribe/<str:subscribe>/<int:period>/', views.SubscribeView.as_view(), name='pay_subscribe_link'),
    path('', include('django.contrib.auth.urls'))
]
