# main/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from courses.models import Course

def home_view(request):
    """Bosh sahifani ko'rsatish uchun view."""
    
    # Bosh sahifada ko'rsatish uchun ikonasi bor oxirgi 3 ta kursni olamiz
    # Bu kurslarni admin paneldan 'featured' (tanlangan) deb belgilash ham mumkin.
    latest_courses = Course.objects.all().order_by('-created_at')[:3]
    
    context = {
        'courses': latest_courses
    }
    return render(request, 'index.html', context)

def login_view(request):
    """Tizimga kirish (login) uchun view."""
    if request.user.is_authenticated:
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """Tizimdan chiqish (logout) uchun view."""
    logout(request)
    return redirect('main:home')

def register_view(request):
    """Yangi foydalanuvchini ro'yxatdan o'tkazish uchun view."""
    if request.user.is_authenticated:
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:dashboard')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'register.html', {'form': form}) # register.html ni keyinroq yaratamiz

def games_view(request):
    """O'yinlar sahifasini ko'rsatish uchun view."""
    return render(request, 'games.html')


def handler404_view(request, exception):
    """
    404 xatoligi uchun maxsus sahifani render qiladi.
    """
    response = render(request, '404.html')
    response.status_code = 404
    return response

