from django.db import models
from django.urls import reverse
from django_resized import ResizedImageField        # resizer image
from django_ckeditor_5.fields import CKEditor5Field  # text editor
from mptt.models import MPTTModel, TreeForeignKey   # MPTT категории

from django.contrib.auth import get_user_model      # model USER
from services.utils import unique_slugify           # use my utils for slug unical
from django.core.validators import FileExtensionValidator # для проверки расширения изображения
from taggit.managers import TaggableManager # Tags
#from services.utils import unique_slugify, image_compress


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
    description = models.TextField(verbose_name='Описание категории', max_length=300, blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Статус')
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория',
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

    class NewsManager(models.Manager):
        """
        Кастомный менеджер для модели статей
        можно добавить еще для СтатьиВКатегорииИподкатегрии
        """
        def all(self):
            """
            Список статей, статья и категория вкл, оптимизация (SQL запрос с фильтрацией)
            """
            return self.get_queryset().filter(is_published=True,
                                              category__is_published=True).\
                select_related('category', 'created_by', 'created_by__profile').prefetch_related('ratings')

        def detail(self):
            """
            Детальная статья (SQL запрос с фильтрацией для страницы со статьёй)
            """
            return self.get_queryset() \
                .select_related('created_by', 'category', 'created_by__profile') \
                .prefetch_related('comments', 'comments__created_by', 'comments__created_by__profile','tags', 'ratings') \
                .filter(is_published=True, category__is_published=True )

    """ Тут можно жестко лажануть, и забыть что обьект переопределен НО только АЛЛ()"""
    objects = NewsManager()   #  переопределяем objects на customNewsManager


    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    short_content = CKEditor5Field(blank=True, verbose_name='Краткое описание', max_length=500)
    content = CKEditor5Field(blank=True, verbose_name='Статья', )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменено')
    photo = ResizedImageField(size=[1920, 1080], crop=['middle', 'center'], upload_to='photos/%Y/%m/%d/',
                              verbose_name='Изображение', blank=True, validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))]
                              )
    is_published = models.BooleanField(default=True, verbose_name='Статус поста')
    created_by = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, verbose_name='Автор',
                                   related_name='author_posts')
    category = TreeForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория', related_name='articles')
    updater = models.ForeignKey(to=User, verbose_name='Обновил', on_delete=models.SET_NULL, null=True,
                                related_name='updater_posts', blank=True)
    fixed = models.BooleanField(verbose_name='Зафиксировано', default=False)
    views = models.IntegerField(default=0, verbose_name='Просмотры', )
    tags = TaggableManager()

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

    # def __init__(self, *args, **kwargs):
    #     ''' Ресайзинг и оптимизация изображения в Django '''
    #     super().__init__(*args, **kwargs)
    #     self.__thumbnail = self.photo if self.pk else None

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        Генератор уникальных SLUG для моделей, в случае существования такого SLUG.
        генерация идет от функции unique_slugify  в sevrvies/utls
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

        # if self.__thumbnail != self.photo and self.photo:
        #     ''' Ресайзинг и оптимизация изображения в Django '''
        #     image_compress(self.photo.path, width=500, height=500)

    def get_sum_rating(self):
        ''' подсчета суммы рейтинг '''
        return sum([rating.value for rating in self.ratings.all()])






class Comment(MPTTModel):
    """
    Модель древовидных комментариев
    """

    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='Статья', related_name='comments')
    created_by = models.ForeignKey(User, verbose_name='Автор комментария', on_delete=models.CASCADE, related_name='comments_created')
    content = models.TextField(verbose_name='Текст комментария', max_length=3000)
    created_at = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Время обновления', auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Статус поста')
    parent = TreeForeignKey('self', verbose_name='Родительский комментарий', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    class MTTMeta:
        # order_insertion_by - сортировка по вложенности
        order_insertion_by = ('-created_at',)

    class Meta:
        indexes = [models.Index(fields=['-created_at', 'updated_at', 'is_published', 'parent'])]
        ordering = ['-created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.created_by}:{self.content}'


class Rating(models.Model):
    """
    Модель рейтинга: Лайк - Дизлайк
    """
    news = models.ForeignKey(to=News, verbose_name='Статья', on_delete=models.CASCADE, related_name='ratings')
    created_by = models.ForeignKey(to=User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True, null=True)
    value = models.IntegerField(verbose_name='Значение', choices=[(1, 'Нравится'), (-1, 'Не нравится')])
    created_at = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    ip_address = models.GenericIPAddressField(verbose_name='IP Адрес')

    class Meta:
        '''  unique_together гарантирует уникальность комбинации article и ip_address. '''
        unique_together = ('news', 'ip_address')
        ordering = ('-created_at',)
        indexes = [models.Index(fields=['-created_at', 'value'])]
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return self.news.title