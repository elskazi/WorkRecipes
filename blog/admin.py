from django.contrib import admin
from .models import News, Category

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','category', 'created_at', 'created_by')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', )

# admin.site.register(News, NewsAdmin)  # other view
# admin.site.register(Category, CategoryAdmin)