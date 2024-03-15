from django import template
from blog.models import Category

register = template.Library()

@register.inclusion_tag('blog/category_menu_sidebar_tpl.html')      # передаем имя шаблон
def show_category_menu(menu_class='uk-list'):                       # передаем дополнительно css
    category_published = Category.objects.filter(is_published=True) # сам запрос для отображения
    return {'category_published':category_published, 'menu_class':menu_class}
