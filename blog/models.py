from django.db import models
from django.urls import reverse
from django_resized import ResizedImageField        # resizer image
from django_ckeditor_5.fields import CKEditor5Field  # text editor
from mptt.models import MPTTModel, TreeForeignKey   # MPTT категории

from django.contrib.auth import get_user_model      # model USER
from services.utils import unique_slugify           # use my utils for slug unical


User = get_user_model()                             # use model USER
"""
о get_user_model() по ссылке
# https://proghunter.ru/articles/django-base-2023-building-a-module-blog-and-model-articles-2
"""


class Category(MPTTModel):
    """
    Модель категорий с вложенностью
    """
    title = models.CharField(max_length=200, verbose_name='Заголовок категории', db_index=True)
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    description = models.TextField(verbose_name='Описание категории', max_length=300)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория'
    )
    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('title',)
    class Meta:
        """
        Сортировка, название модели в админ панели, таблица в данными
        """
        verbose_name = 'Категория'  # Имя модели в единственном числе
        verbose_name_plural = 'Категории'  # Имя модели в множ. числе
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('blog:news_by_category', kwargs={'slug': self.slug}) #kwargs={"category_id": self.pk, }, )

    def __str__(self):
        """
        Возвращение заголовка статьи
        """
        return self.title


class News(models.Model):
    """
    Модель постов для сайта
    """

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    short_content = CKEditor5Field(blank=True, verbose_name='Краткое описание', max_length=500)
    content = CKEditor5Field(blank=True, verbose_name='Статья', )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено')
    photo = ResizedImageField(size=[1920, 1080], crop=['middle', 'center'], upload_to='photos/%Y/%m/%d/',
                              verbose_name='Изображение', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Статус поста')
    created_by = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, verbose_name='Автор',
                                   related_name='author_posts')
    category = TreeForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория', related_name='articles')
    updater = models.ForeignKey(to=User, verbose_name='Обновил', on_delete=models.SET_NULL, null=True,
                                related_name='updater_posts', blank=True)
    fixed = models.BooleanField(verbose_name='Зафиксировано', default=False)
    views = models.IntegerField(default=0, verbose_name='Просмотры', )

    class Meta:
        verbose_name = 'Новость'  # Имя модели в единственном числе
        verbose_name_plural = 'Новости'  # Имя модели в множ. числе
        indexes = [models.Index(fields=['-fixed', '-created_at', 'is_published'])]
        ordering = ['-fixed', '-created_at', 'title']

    def get_absolute_url(self):
        """Создаем ссылку на статью, через SLUG. в шаблоне меняем {% url '' %} на {{ item.get_absolute_url }}"""
        return reverse('blog:news_details', kwargs={'slug': self.slug})

    def __str__(self):
        """
        Возвращение заголовка статьи
        """
        return self.title

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        Генератор уникальных SLUG для моделей, в случае существования такого SLUG.
        генерация идет от функции unique_slugify  в sevrvies/utls
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)