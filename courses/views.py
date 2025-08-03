# courses/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import Course, Lesson, Enrollment, Module, ModuleProgress, Certificate, LessonProgress
import json
from django.http import JsonResponse, HttpResponseBadRequest
from .models import FillTheBlankExercise
# --- YORDAMCHI FUNKSIYALAR ---

def update_module_progress(enrollment, module):
    """
    Berilgan modulning o'zlashtirish progressini hisoblaydi va yangilaydi.
    """
    total_lessons_in_module = Lesson.objects.filter(module=module).count()
    completed_lessons_in_module = LessonProgress.objects.filter(
        enrollment=enrollment, 
        lesson__module=module, 
        is_completed=True
    ).count()

    progress = (completed_lessons_in_module / total_lessons_in_module) * 100 if total_lessons_in_module > 0 else 0
    
    module_progress, created = ModuleProgress.objects.get_or_create(
        enrollment=enrollment, 
        module=module
    )
    module_progress.progress = progress
    module_progress.is_completed = (progress == 100)
    module_progress.save()

def update_course_progress(enrollment):
    """
    Kursning umumiy o'zlashtirish progressini hisoblaydi va yakunlangan bo'lsa,
    sertifikat yaratadi.
    """
    total_modules_in_course = Module.objects.filter(course=enrollment.course).count()
    completed_modules_in_course = ModuleProgress.objects.filter(
        enrollment=enrollment,
        is_completed=True
    ).count()

    progress = (completed_modules_in_course / total_modules_in_course) * 100 if total_modules_in_course > 0 else 0
    
    enrollment.progress = progress
    
    if progress == 100:
        enrollment.is_completed = True
        # Kurs tugagani uchun sertifikat yaratamiz yoki olamiz
        Certificate.objects.get_or_create(enrollment=enrollment)

    enrollment.save()


# --- ASOSIY VIEW FUNKSIYALARI ---

@login_required
def course_list_view(request):
    """Barcha mavjud kurslar ro'yxatini ko'rsatish."""
    all_courses = Course.objects.all().order_by('created_at')
    enrolled_course_ids = Enrollment.objects.filter(user=request.user).values_list('course_id', flat=True)
    
    context = {
        'courses': all_courses,
        'enrolled_course_ids': list(enrolled_course_ids),
    }
    return render(request, 'course_list.html', context)

@login_required
def course_detail_view(request, course_id):
    """
    Kursning detal sahifasi. Foydalanuvchi yozilgan bo'lsa, birinchi o'tilmagan
    darsga yo'naltiradi. Yozilmagan bo'lsa, kursga yozilish sahifasini ko'rsatadi.
    """
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)

    if created:
        # Agar foydalanuvchi endi yozilgan bo'lsa, uni yozilish sahifasiga emas,
        # to'g'ridan-to'g'ri darsga yo'naltiramiz.
        # Bu 'enroll_view' funksiyasiga ehtiyojni kamaytiradi.
        pass

    # O'tilmagan birinchi darsni topish logikasi
    completed_lessons_ids = LessonProgress.objects.filter(enrollment=enrollment, is_completed=True).values_list('lesson_id', flat=True)
    
    # Barcha darslarni tartib bilan olish
    all_lessons = Lesson.objects.filter(module__course=course).order_by('module__order', 'order')
    
    next_lesson = None
    for lesson in all_lessons:
        if lesson.id not in completed_lessons_ids:
            next_lesson = lesson
            break

    if next_lesson:
        return redirect('courses:lesson_detail', course_id=course.id, lesson_id=next_lesson.id)
    elif all_lessons.exists():
        # Barcha darslar tugatilgan, sertifikat sahifasiga yuboramiz
        return redirect('courses:view_certificate', course_id=course.id)
    else:
        # Kursda hali darslar yo'q
        return render(request, 'no_lessons.html', {'course': course}) # no_lessons.html shablonini yaratish kerak

@login_required
def lesson_detail_view(request, course_id, lesson_id):
    """Muayyan bitta darsni ko'rsatish."""
    course = get_object_or_404(Course, id=course_id)
    active_lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

    if not enrollment:
        return HttpResponseForbidden("Siz bu kursga yozilmagansiz.")
        
    lesson_progress, created = LessonProgress.objects.get_or_create(
        enrollment=enrollment, 
        lesson=active_lesson
    )

    # O'TILGAN DARSLAR RO'YXATINI SHU YERDA TAYYORLAYMIZ
    completed_lesson_ids = list(
        enrollment.lesson_progresses.filter(is_completed=True).values_list('lesson_id', flat=True)
    )

    context = {
        'course': course,
        'active_lesson': active_lesson,
        'lesson_progress': lesson_progress,
        'completed_lesson_ids': completed_lesson_ids, # <-- TAYYOR RO'YXATNI KONTEKSTGA QO'SHDIK
    }
    return render(request, 'course-detail.html', context)

@login_required
def complete_lesson_view(request, lesson_id):
    """Darsni 'tugatildi' deb belgilash va progressni yangilash."""
    if request.method == 'POST':
        lesson = get_object_or_404(Lesson, id=lesson_id)
        enrollment = get_object_or_404(Enrollment, user=request.user, course=lesson.module.course)
        
        # Dars progressini "tugatildi" deb belgilaymiz
        lesson_progress, created = LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
        lesson_progress.is_completed = True
        lesson_progress.save()

        # Ushbu dars tegishli bo'lgan modul progressini yangilaymiz
        update_module_progress(enrollment, lesson.module)
        
        # Kursning umumiy progressini yangilaymiz
        update_course_progress(enrollment)

        # Keyingi darsni topish
        next_lesson = Lesson.objects.filter(
            module__course=lesson.module.course,
            module__order__gte=lesson.module.order
        ).exclude(id=lesson.id).order_by('module__order', 'order').first()

        if next_lesson:
            return redirect('courses:lesson_detail', course_id=lesson.module.course.id, lesson_id=next_lesson.id)
        else:
            # Bu oxirgi dars edi. Kurs tugadi.
            return redirect('courses:view_certificate', course_id=lesson.module.course.id)

    return redirect('users:dashboard') # POST bo'lmasa, dashboard'ga qaytish

@login_required
def view_certificate_view(request, course_id):
    """Kurs uchun sertifikatni ko'rish."""
    course = get_object_or_404(Course, id=course_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

    if not enrollment.is_completed:
        return HttpResponseForbidden("Sertifikatni ko'rish uchun avval kursni to'liq tugating.")

    certificate, created = Certificate.objects.get_or_create(enrollment=enrollment)
    
    context = {
        'certificate': certificate
    }
    return render(request, 'certificate.html', context)

# enroll_view endi shart emas, chunki course_detail_view uning vazifasini bajarmoqda.
# Agar alohida "Kursga yozilish" sahifasi kerak bo'lsa, saqlab qolish mumkin.
@login_required
def enroll_view(request, course_id):
    """Foydalanuvchini kursga yozish."""
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('courses:detail', course_id=course.id)



@login_required
def check_exercise_view(request, exercise_id):
    """
    AJAX orqali kelgan amaliy topshiriq javobini tekshiradi va JSON javob qaytaradi.
    """
    if request.method == 'POST':
        try:
            exercise = get_object_or_404(FillTheBlankExercise, id=exercise_id)
            data = json.loads(request.body)
            user_answer = data.get('answer', '').strip()

            if not user_answer:
                return JsonResponse({'correct': False, 'message': 'Javob kiritilmadi.'})

            # Javobni katta-kichik harflarga e'tibor bermaydigan qilib tekshiramiz
            if user_answer.lower() == exercise.correct_answer.lower():
                # Kelajakda bu yerga yutuq (achievement) berish logikasini qo'shish mumkin
                return JsonResponse({'correct': True, 'message': 'Toʻppa-toʻgʻri! Barakalla!'})
            else:
                return JsonResponse({'correct': False, 'message': 'Xato. Yana bir bor urinib koʻring.'})

        except FillTheBlankExercise.DoesNotExist:
            return JsonResponse({'error': 'Topshiriq topilmadi.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Notoʻgʻri soʻrov formati.'}, status=400)

    return HttpResponseBadRequest("Faqat POST so'rovlariga ruxsat etiladi.")