from django.contrib import admin
from django.urls import path, include

"""Подключение статики и медиа."""
from config import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ckeditor5/', include('django_ckeditor_5.urls')), # text editor
    path('admin/', admin.site.urls),
    path('', include('blog.urls'))
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
