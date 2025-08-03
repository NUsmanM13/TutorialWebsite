# main/urls.py

from django.urls import path
from . import views  # Hali yaratilmagan, lekin keyingi qadamda yaratamiz

app_name = 'main'

urlpatterns = [
    # Bosh sahifa uchun (masalan: yoursite.com/)
    path('', views.home_view, name='home'),
    
    # Tizimga kirish sahifasi (masalan: yoursite.com/login/)
    path('login/', views.login_view, name='login'),
    
    # Tizimdan chiqish uchun
    path('logout/', views.logout_view, name='logout'),
    
    # Ro'yxatdan o'tish sahifasi (masalan: yoursite.com/register/)
    path('register/', views.register_view, name='register'),
    
    # O'yinlar sahifasi (masalan: yoursite.com/games/)
    path('games/', views.games_view, name='games'),
]