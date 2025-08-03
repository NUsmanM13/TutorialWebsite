# users/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Certificate,Course

@login_required
def dashboard_view(request):
    """Foydalanuvchining shaxsiy panelini ko'rsatish."""
    
    # Yutuq sifatida ko'rsatiladigan barcha kurslarni olamiz (ikonasi borlarni)
    all_achievements = Course.objects.filter(icon_class__isnull=False).exclude(icon_class__exact='')

    # Foydalanuvchi tamomlagan kurslarning ID'larini olamiz
    completed_courses_ids = request.user.enrollments.filter(is_completed=True).values_list('course_id', flat=True)

    context = {
        'all_achievements': all_achievements,
        'completed_courses_ids': list(completed_courses_ids)
    }
    return render(request, 'dashboard.html', context)

@login_required
def my_certificates_view(request):
    """Foydalanuvchining barcha sertifikatlarini ko'rsatish."""
    certificates = Certificate.objects.filter(enrollment__user=request.user)
    context = {
        'certificates': certificates
    }
    # Bu shablonni ham keyinroq yaratamiz
    return render(request, 'my_certificates.html', context)

@login_required
def download_certificate_view(request, certificate_id):
    """
    Sertifikatni PDF formatda yuklab olish (hozircha HTML ko'rinishida).
    PDF generatsiya qilish uchun WeasyPrint yoki ReportLab kabi kutubxonalar kerak.
    """
    certificate = get_object_or_404(
        Certificate, 
        id=certificate_id, 
        enrollment__user=request.user # Faqat o'zining sertifikatini yuklay oladi
    )
    # Hozircha oddiy sertifikat sahifasiga yo'naltiramiz
    return render(request, 'certificate.html', {'certificate': certificate})