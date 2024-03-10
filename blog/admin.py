from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin # Вложенные категори МРТТ
from .models import News, Category

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','category', 'created_at', 'created_by')
    list_display_links = ('id', 'title')

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'id', 'title', 'slug',)
    list_display_links = ('id', 'title', 'slug',)
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Основная инфрмация', {'fields':('title', 'slug', 'parent')}),
        ('Описание', {'fields': ('description',)}),
    )

# admin.site.register(News, NewsAdmin)  # other view
# admin.site.register(Category, CategoryAdmin)



















