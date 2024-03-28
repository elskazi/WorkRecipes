from django import template
from django.db.models import Count
from taggit.models import Tag
from ..models import Comment # blog.models

register = template.Library()

@register.simple_tag
def popular_tags():
    """
    получаем список популярных тегов, отсортированных по количеству статей,
    содержащих эти теги.  Используется модуль django.db.models (Count) для выполнения
    запросов к базе данных Django и модель Tag из стороннего пакета django-taggit для работы с тегами.

    После выполнения запроса, полученный список тегов сохраняется в переменной tag_list.
    Каждый элемент списка представлен в виде словаря, содержащего три ключа - name (имя тега),
    num_times (количество статей с этим тегом) и slug (уникальный идентификатор тега).
    """
    tags = Tag.objects.annotate(num_times=Count('news')).order_by('-num_times')
    tag_list = list(tags.values('name', 'num_times', 'slug'))
    return tag_list

@register.inclusion_tag('blog/inc/latest_comments.html')
def show_latest_comments(count=5):
    """
    Тег использует Comment.objects.select_related('created_by'),
    чтобы получить последние комментарии, связанные с их авторами.
    Фильтр filter(is_published=True) используется для получения только опубликованных комментариев.
    Комментарии сортируются по дате создания в обратном порядке с помощью order_by('-created_at').
    """
    comments = Comment.objects.select_related('created_by').filter(is_published=True).order_by('-created_at')[:count]
    return {'comments': comments}