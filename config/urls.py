from django.contrib import admin
from django.urls import path, include

from config import settings  # Подключение статики и медиа.
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap  # sitemap
from blog.sitemaps import StaticSitemap, ArticleSitemap  # sitemap

sitemaps = {                        # map site
    'static': StaticSitemap,
    'articles': ArticleSitemap,
}

handler403 = 'system.views.tr_handler403'   # стр ошибок
handler404 = 'system.views.tr_handler404'
handler500 = 'system.views.tr_handler500'

urlpatterns = [
    path('ckeditor5/', include('django_ckeditor_5.urls')),  # text editor
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('blog.urls')),
    path('', include('system.urls')),
]
if settings.DEBUG:
    """Подключение статики и медиа. вариант +=  И  .extend """
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.extend(
        static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    )
    urlpatterns.append(
        path('__debug__/', include('debug_toolbar.urls'))
    )

'''
другой вариант подключения
if settings.DEBUG:
    urlpatterns = [path('__debug__/', include('debug_toolbar.urls'))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
