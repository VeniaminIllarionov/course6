from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(verbose_name='Описание')
    slug = models.CharField(max_length=150, verbose_name='Slug', null=True, blank=True)
    preview = models.ImageField(upload_to='blogentry/photo', verbose_name='Изображение', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    sign_publication = models.IntegerField(default=0, verbose_name='Просмотры')
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
