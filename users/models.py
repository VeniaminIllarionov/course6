from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта')

    first_name = models.CharField(max_length=150, verbose_name='Имя')

    last_name = models.CharField(max_length=150, verbose_name='Фамилия')

    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', blank=True, null=True,
                               help_text='Загрузите свой аватар')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', blank=True,
                             null=True, help_text='Введите номер телефона')
    country = models.CharField(max_length=35, verbose_name='Страна', blank=True,
                               null=True, help_text='Введите страну')
    token = models.CharField(max_length=100, verbose_name='Токен', blank=True, null=True, )

    is_block = models.BooleanField(default=False, verbose_name='Блокировка пользователя')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('view_users', 'Может просматривать список пользователей сервиса.'),
                       ('change_is_block', 'Может блокировать пользователей сервиса.')
                       ]

    def __str__(self):
        return f'{self.email}'
