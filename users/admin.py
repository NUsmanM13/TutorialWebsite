# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Foydalanuvchi modelini admin panelda sozlash.
    """
    # Foydalanuvchilar ro'yxatida ko'rinadigan ustunlar
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    # Qidiruv maydonlari
    search_fields = ('username', 'email', 'first_name', 'last_name')
    # Filtrlash maydonlari
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    # UserAdmin'dagi standart fieldsets'ni ishlatamiz, agar o'zgartirish kerak bo'lsa
    # bu yerdan o'zgartiriladi. Hozircha standart holati bizga yetarli.
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets