# Generated by Django 5.0.6 on 2024-06-30 20:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='next_day',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Следующая отправка рассылки'),
        ),
    ]
