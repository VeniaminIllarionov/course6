# Generated by Django 4.2 on 2024-07-03 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, help_text='Загрузите свой аватар', null=True, upload_to='users/photo', verbose_name='Аватар'),
        ),
    ]
