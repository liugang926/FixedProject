from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.get_user_info, name='user-info'),
    path('logout/', views.user_logout, name='user-logout'),
] 