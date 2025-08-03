# main/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username': 'Login (foydalanuvchi nomi)',
            'first_name': 'Ismingiz',
            'last_name': 'Familiyangiz',
            'email': 'Elektron pochta',
        }