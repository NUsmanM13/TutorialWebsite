# users/urls.py

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Foydalanuvchining boshqaruv paneli (masalan: yoursite.com/dashboard/)
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Foydalanuvchining barcha sertifikatlarini ko'radigan sahifa
    path('my-certificates/', views.my_certificates_view, name='my_certificates'),
    
    # Muayyan sertifikatni yuklab olish uchun (bu yerda unikal ID ishlatiladi)
    path('certificate/<uuid:certificate_id>/download/', views.download_certificate_view, name='download_certificate'),
]