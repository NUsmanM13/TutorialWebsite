# courses/models.py

import uuid
from django.db import models
from django.conf import settings
# Fayl yuklash imkoniyatiga ega RichTextUploadingField'ni import qilamiz
from ckeditor_uploader.fields import RichTextUploadingField

class Course(models.Model):
    """Kurslar uchun model"""
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses_taught',
        verbose_name="O'qituvchi"
    )
    title = models.CharField(max_length=200, verbose_name="Kurs sarlavhasi")
    description = models.TextField(verbose_name="Kurs haqida ma'lumot")
    image = models.ImageField(upload_to='course_images/', blank=True, null=True, verbose_name="Kurs rasmi")

    icon_class = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name="Yutuq Ikonasi Klassi (BoxIcons)",
        help_text="Masalan: bxl-python, bxl-javascript"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Module(models.Model):
    """Kurs ichidagi modullar uchun model"""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name="Kurs"
    )
    title = models.CharField(max_length=200, verbose_name="Modul sarlavhasi")
    order = models.PositiveIntegerField(verbose_name="Tartib raqami")

    class Meta:
        verbose_name = "Modul"
        verbose_name_plural = "Modullar"
        ordering = ['course', 'order']
        unique_together = ('course', 'order')

    def __str__(self):
        return f"{self.course.title} - Modul {self.order}: {self.title}"

class Lesson(models.Model):
    """Modul ichidagi darslar uchun model"""
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name="Modul"
    )
    title = models.CharField(max_length=200, verbose_name="Dars sarlavhasi")
    # O'ZGARTIRILDI: Endi bu maydon fayl yuklash imkoniyatiga ega
    content = RichTextUploadingField(verbose_name="Dars kontenti")
    order = models.PositiveIntegerField(verbose_name="Tartib raqami")

    class Meta:
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
        ordering = ['module', 'order']
        unique_together = ('module', 'order')

    def __str__(self):
        return f"{self.module.title} - Dars {self.order}: {self.title}"

class LessonMaterial(models.Model):
    """Darsga biriktirilgan fayllar uchun model"""
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='materials',
        verbose_name="Dars"
    )
    title = models.CharField(max_length=150, verbose_name="Material nomi")
    file = models.FileField(upload_to='lesson_materials/', verbose_name="Fayl")

    class Meta:
        verbose_name = "Dars materiali"
        verbose_name_plural = "Dars materiallari"

    def __str__(self):
        return self.title

class FillTheBlankExercise(models.Model):
    """Dars uchun "tushirib qoldirilgan so'z" topshirig'i"""
    lesson = models.OneToOneField(
        Lesson,
        on_delete=models.CASCADE,
        related_name='exercise',
        verbose_name="Dars"
    )
    # Misol: "Django - bu ____ freymvorki."
    question_text = models.TextField(
        verbose_name="Savol matni",
        help_text="Tushirib qoldirilgan so'z o'rniga {blank} yozing."
    )
    correct_answer = models.CharField(max_length=100, verbose_name="To'g'ri javob")

    class Meta:
        verbose_name = "Amaliy topshiriq (bo'shliqni to'ldirish)"
        verbose_name_plural = "Amaliy topshiriqlar (bo'shliqni to'ldirish)"

    def __str__(self):
        return f"{self.lesson.title} uchun topshiriq"

class Enrollment(models.Model):
    """Foydalanuvchining kursga yozilishi"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name="Foydalanuvchi"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name="Kurs"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="Yozilgan vaqti")
    progress = models.FloatField(default=0.0, verbose_name="O'zlashtirish progressi (%)")
    is_completed = models.BooleanField(default=False, verbose_name="Tugatilganmi")

    class Meta:
        verbose_name = "Kursga yozilish"
        verbose_name_plural = "Kursga yozilishlar"
        unique_together = ('user', 'course') # Bir foydalanuvchi bir kursga faqat bir marta yozilishi mumkin

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

class ModuleProgress(models.Model):
    """Foydalanuvchining modul bo'yicha progressi"""
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='module_progresses'
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    progress = models.FloatField(default=0.0)

    class Meta:
        verbose_name = "Modul progressi"
        verbose_name_plural = "Modul progresslari"
        unique_together = ('enrollment', 'module')

    def __str__(self):
        return f"{self.enrollment} - {self.module.title} Progress"


class Certificate(models.Model):
    """Kursni tugatganlik haqidagi sertifikat modeli"""
    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='certificate',
        verbose_name="Kursga yozilish"
    )
    certificate_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="Unikal ID")
    issued_at = models.DateField(auto_now_add=True, verbose_name="Berilgan sana")
    certificate_file = models.FileField(upload_to='certificates/', verbose_name="Sertifikat fayli")

    class Meta:
        verbose_name = "Sertifikat"
        verbose_name_plural = "Sertifikatlar"

    def __str__(self):
        return f"{self.enrollment.user.username} uchun {self.enrollment.course.title} sertifikati"



# courses/models.py faylining oxiriga qo'shing

class LessonProgress(models.Model):
    """Foydalanuvchining har bir dars bo'yicha progressi"""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progresses')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Dars progressi"
        verbose_name_plural = "Dars progresslari"
        unique_together = ('enrollment', 'lesson')

    def __str__(self):
        return f"{self.enrollment} - {self.lesson.title}"