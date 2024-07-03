# Generated by Django 4.2 on 2024-07-02 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0003_mailing_next_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailing_attempt',
            name='is_active',
        ),
        migrations.AddField(
            model_name='mailing',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Статус Рассылки'),
        ),
    ]