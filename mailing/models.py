from django.db import models, connection


# Create your models here.
class Mailing(models.Model):
    mailing_id = models.AutoField(primary_key=True, verbose_name='id рассылки')
    send_mailing_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время первой отправки рассылки')
    frequency = models.IntegerField(verbose_name='периодичность')
    mailing_status = models.BooleanField(default=False, verbose_name='статус рассылки')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f'{self.mailing_id}:{self.send_mailing_at} - {self.frequency} - {self.mailing_status}'


class Customers(models.Model):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    fio = models.CharField(max_length=50, verbose_name='ФИО')
    comment = models.TextField(blank=True, verbose_name='Коммент')
    mailing_id = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='id рассылки')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.fio}: {self.email} - {self.comment}'


class Massage(models.Model):
    mailing_id = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='id рассылки')
    subject_massage = models.CharField(max_length=80, verbose_name='Тема письма')
    massage = models.TextField(verbose_name='Текст письма')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.mailing_id}:{self.subject_massage} - {self.massage}'


class Mailing_attempt(models.Model):
    last_attempt = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    status = models.BooleanField(default=False, verbose_name='статус попытки')
    mail_response = models.CharField(max_length=50, verbose_name='ответ почтового сервера')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'
