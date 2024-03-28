from django import template
from blog.models import Category

register = template.Library()

@register.inclusion_tag('blog/inc/category_menu_sidebar_tpl.html')
def show_category_menu(menu_class='uk-list'):
    category_published = Category.objects.filter(is_published=True)
    return {'category_published':category_published, 'menu_class':menu_class}
