# Generated by Django 4.2.2 on 2024-06-27 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing_attempt',
            name='mail_response',
            field=models.CharField(choices=[('per_day', 'раз в день'), ('per_week', 'раз в неделю'), ('per_month', 'раз в месяц')], default='per_day', max_length=50, verbose_name='ответ почтового сервера'),
        ),
        migrations.AlterField(
            model_name='mailing_attempt',
            name='status',
            field=models.CharField(choices=[('created', 'создана'), ('executing', 'запущена'), ('finished', 'закончена успешно'), ('error', 'законечена с ошибками')], default='created', verbose_name='статус попытки'),
        ),
    ]