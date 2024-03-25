from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin # Вложенные категори МРТТ
from .models import News, Category, Comment

# изменение формата дат в админке в приложении данном
from django.conf.locale.ru import formats as ru_formats
ru_formats.DATETIME_FORMAT = "d.m.Y H:i"


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','category', 'is_published', 'created_by', 'created_at')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}      # auto use slug in admin
    list_editable = ('is_published',)               # чекбоксы для публикации
    # readonly_fields =
    list_filter = ('is_published', 'category',)     # боковой фильтр
    search_fields = ('title',)
    save_on_top = True
    #save_as = True

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'id', 'title','is_published', 'slug',)
    list_display_links = ('id', 'title', 'slug',)
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True
    fieldsets = (
        ('Основная инфрмация', {'fields':('title', 'slug', 'parent','is_published')}),
        ('Описание', {'fields': ('description',)}),
    )

@admin.register(Comment)
class CommentAdminPage(DraggableMPTTAdmin):
    """
    Админ-панель модели комментариев
    """
    list_display = ('tree_actions', 'indented_title', 'news', 'created_by', 'created_at', 'is_published')
    mptt_level_indent = 2
    list_display_links = ('news',)
    list_filter = ('created_at', 'updated_at', 'created_by')
    list_editable = ('is_published',)

# admin.site.register(News, NewsAdmin)  # other view
# admin.site.register(Category, CategoryAdmin)



















