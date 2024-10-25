from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(verbose_name='автар', **NULLABLE)
    country = models.CharField(max_length=55, verbose_name='страна', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            ('view_clients_list', 'Может просматривать список пользователей сервиса'),
            ('update_is_blocked', 'Может блокировать пользователей сервиса'),
        ]



