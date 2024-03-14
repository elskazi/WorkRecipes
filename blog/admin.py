from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin # Вложенные категори МРТТ
from .models import News, Category

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','category', 'created_at', 'created_by')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}      # auto use slug in admin
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

# admin.site.register(News, NewsAdmin)  # other view
# admin.site.register(Category, CategoryAdmin)



















