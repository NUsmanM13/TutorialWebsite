# courses/urls.py

from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Barcha kurslar ro'yxatini ko'rsatadigan sahifa (masalan: yoursite.com/courses/)
    path('', views.course_list_view, name='list'),

    # Muayyan bitta kurs haqida batafsil ma'lumot sahifasi (masalan: yoursite.com/courses/1/)
    path('<int:course_id>/', views.course_detail_view, name='detail'),
    
    # Muayyan kursning ichidagi muayyan darsni ko'rish (masalan: yoursite.com/courses/1/lesson/5/)
    path('<int:course_id>/lesson/<int:lesson_id>/', views.lesson_detail_view, name='lesson_detail'),
    
    # Kursga yozilish (bu odatda tugma bosilganda fon rejimida ishlaydi)
    path('<int:course_id>/enroll/', views.enroll_view, name='enroll'),
    
    # Darsni "tugatildi" deb belgilash uchun
    path('lesson/<int:lesson_id>/complete/', views.complete_lesson_view, name='complete_lesson'),

    path('exercise/check/<int:exercise_id>/', views.check_exercise_view, name='check_exercise'),
    # Kursni tugatgandan so'ng sertifikatni generatsiya qilish va ko'rish sahifasi
    path('<int:course_id>/certificate/', views.view_certificate_view, name='view_certificate'),
]