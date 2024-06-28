from django.db import models, connection

from users.models import User


# Create your models here.
class Mailing(models.Model):
    period_variants = (
        ('per_day', 'раз в день'),
        ('per_week', 'раз в неделю'),
        ('per_month', 'раз в месяц')
    )

    send_mailing_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время первой отправки рассылки')
    frequency = models.CharField(max_length=50, choices=period_variants, default='per_day',
                                 verbose_name='периодичность')
    mailing_status = models.CharField(max_length=80, verbose_name='статус рассылки')

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Пользователь', null=True, blank=True)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f'{self.send_mailing_at} - {self.frequency} - {self.mailing_status}'


class Customers(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    fio = models.CharField(max_length=50, verbose_name='ФИО')
    comment = models.TextField(blank=True, verbose_name='Коммент')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.fio}: {self.email} - {self.comment}'


class Massage(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    subject_massage = models.CharField(max_length=80, verbose_name='Тема письма')
    massage = models.TextField(verbose_name='Текст письма')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        permissions = [
            ('view_mailing', 'Может просматривать любые рассылки.')]

    def __str__(self):
        return f'{self.subject_massage} - {self.massage}'


class Mailing_attempt(models.Model):
    status_variants = (
        ('created', 'создана'),
        ('executing', 'запущена'),
        ('finished', 'закончена успешно'),
        ('error', 'законечена с ошибками')
    )

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    last_attempt = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    status = models.CharField(choices=status_variants, default='created', verbose_name='статус попытки')
    mail_response = models.CharField(max_length=50, verbose_name='ответ почтового сервера')
    is_active = models.BooleanField(default=True, verbose_name='Статус Рассылки')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'
        permissions = [
            ('can_edit_is_active', 'Может отключать рассылки.'), ]

    def __str__(self):
        return f'{self.last_attempt} - {self.status} - {self.mail_response}'
