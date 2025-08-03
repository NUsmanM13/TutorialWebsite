# courses/admin.py

from django.contrib import admin
from .models import (
    Course,
    Module,
    Lesson,
    LessonMaterial,
    FillTheBlankExercise,
    Enrollment,
    ModuleProgress,
    Certificate,
)

# --- INLINE KLASSLARI ---
# Bular boshqa modelning ichida ko'rsatish uchun xizmat qiladi.

class ModuleInline(admin.TabularInline):
    """Kurs sahifasida Modullarni tahrirlash uchun inline."""
    model = Module
    extra = 1  # Standart nechta qo'shimcha bo'sh forma ko'rsatish
    verbose_name = "Modul"
    verbose_name_plural = "Modullar"


class LessonMaterialInline(admin.TabularInline):
    """Dars sahifasida Materiallarni tahrirlash uchun inline."""
    model = LessonMaterial
    extra = 1
    verbose_name = "Darsga material"
    verbose_name_plural = "Darsga materiallar"


class FillTheBlankExerciseInline(admin.StackedInline):
    """Dars sahifasida Amaliy topshiriqni tahrirlash uchun inline."""
    model = FillTheBlankExercise
    # StackedInline OneToOne maydonlar uchun chiroyliroq ko'rinadi
    can_delete = False # O'chirish mumkin emas, chunki bu OneToOne
    verbose_name = "Amaliy topshiriq (bo'shliqni to'ldirish)"


class ModuleProgressInline(admin.TabularInline):
    """Kursga yozilish sahifasida Modul progresslarini ko'rsatish uchun."""
    model = ModuleProgress
    extra = 0
    # Bu maydonlarni admin o'zgartirmasligi kerak, ular avtomatik hisoblanadi
    readonly_fields = ('module', 'progress', 'is_completed')
    can_delete = False # Progressni o'chirib bo'lmaydi

    def has_add_permission(self, request, obj=None):
        # Progress qo'lda qo'shilmasligi kerak
        return False


# --- ASOSIY ADMIN KLASSLARI ---

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Kurs modelini admin panelda sozlash."""
    # 'icon_class' ni ro'yxatga qo'shamiz
    list_display = ('title', 'instructor', 'icon_class', 'created_at')
    list_filter = ('instructor', 'created_at')
    search_fields = ('title', 'description', 'instructor__username')
    inlines = [ModuleInline]
    
    # Uni tahrirlash formasiga ham qo'shamiz
    fieldsets = (
        (None, {
            'fields': ('title', 'instructor', 'description', 'image')
        }),
        ('Yutuqlar Sozlamasi', {
            'fields': ('icon_class',)
        }),
    )


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """Modul modelini admin panelda sozlash."""
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    list_editable = ('order',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Dars modelini admin panelda sozlash."""
    list_display = ('title', 'module', 'order')
    list_filter = ('module__course', 'module')
    search_fields = ('title', 'content', 'module__title')
    list_editable = ('order',)
    # Dars sahifasida uning materiallari va topshiriqlarini ko'rsatamiz
    inlines = [LessonMaterialInline, FillTheBlankExerciseInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Kursga yozilish modelini admin panelda sozlash."""
    list_display = ('user', 'course', 'progress', 'is_completed', 'enrolled_at')
    list_filter = ('course', 'is_completed')
    search_fields = ('user__username', 'course__title')
    readonly_fields = ('enrolled_at', 'progress', 'is_completed')
    # Kursga yozilish holatini ko'rayotganda modullar progressini ham ko'ramiz
    inlines = [ModuleProgressInline]

    def get_readonly_fields(self, request, obj=None):
        # Agar obyekt yangi yaratilayotgan bo'lsa, ba'zi maydonlar ochiq bo'ladi
        if obj: # obj mavjud bo'lsa (tahrirlash rejimi)
            return self.readonly_fields + ('user', 'course')
        return self.readonly_fields


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    """Sertifikat modelini admin panelda sozlash."""
    list_display = ('get_user', 'get_course', 'issued_at', 'certificate_id')
    search_fields = ('enrollment__user__username', 'enrollment__course__title')
    # Sertifikatlar tizim tomonidan avtomatik yaratilishi kerak,
    # shuning uchun admin panelda ularni faqat ko'rish mumkin bo'lgani ma'qul.
    readonly_fields = ('enrollment', 'certificate_id', 'issued_at', 'certificate_file')

    def get_user(self, obj):
        return obj.enrollment.user
    get_user.short_description = "Foydalanuvchi"
    get_user.admin_order_field = 'enrollment__user'

    def get_course(self, obj):
        return obj.enrollment.course
    get_course.short_description = "Kurs"
    get_course.admin_order_field = 'enrollment__course'

    def has_add_permission(self, request):
        # Admin panel orqali sertifikat qo'shishni taqiqlaymiz
        return False

# Qolgan modellarni ham ro'yxatdan o'tkazamiz, agar ularga alohida kirish kerak bo'lsa.
# Lekin biz ularni inline qilganimiz uchun bu shart emas. Agar alohida menyu
# sifatida kerak bo'lsa, izohdan ochishingiz mumkin.
# admin.site.register(LessonMaterial)
# admin.site.register(FillTheBlankExercise)
# admin.site.register(ModuleProgress)