from django.db import models

# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='заголовок')
    slug = models.CharField(max_length=500, **NULLABLE, verbose_name='slug')
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='img/', **NULLABLE, verbose_name='превью')
    created_at = models.DateTimeField(auto_now_add=True , verbose_name='время создания')
    is_published = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)


    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    def __str__(self):
        return self.title