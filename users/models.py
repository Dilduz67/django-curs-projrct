from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(max_length=150, verbose_name="логин",unique=True,validators=[username_validator],error_messages={"unique": ("A user with that username already exists.")})
    email = models.EmailField(unique=False, verbose_name='почта',**NULLABLE)

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
