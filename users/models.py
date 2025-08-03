# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Django'ning standart User modelini kengaytiruvchi model.
    Kelajakda bio, profil rasmi kabi maydonlar qo'shilishi mumkin.
    """
    email = models.EmailField(unique=True, verbose_name="Elektron pochta")

    def __str__(self):
        return self.username