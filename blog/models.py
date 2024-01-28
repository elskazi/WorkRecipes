from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок категории', db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.pk, }, )

    class Meta:
        verbose_name = 'Категория'  # Имя модели в единственном числе
        verbose_name_plural = 'Категории'  # Имя модели в множ. числе
        ordering = ['title']

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(blank=True, verbose_name='Контент', )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Изображение', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_by = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
    archived = models.BooleanField(default=False, verbose_name='В архив')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория', related_name='category'  )
    views = models.IntegerField(default=0, verbose_name='Просмотры', )

    class Meta:
        verbose_name = 'Новость'  # Имя модели в единственном числе
        verbose_name_plural = 'Новости'  # Имя модели в множ. числе
        ordering = ['-created_at', 'title']

    # def get_absolute_url(self):
    #     return reverse('view_news', kwargs={"pk": self.pk, }, ) Еще нет имени ссылки

    def __str__(self):
        return self.title
