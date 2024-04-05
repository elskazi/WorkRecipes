from uuid import uuid4
from pytils.translit import slugify

import os   # для пути сохранения изобраджений Редактора
from django.core.files.storage import FileSystemStorage
from config import settings
from urllib.parse import urljoin
from datetime import datetime

from PIL import Image, ImageOps  # Ресайзинг и оптимизация изображения в Django, не использую из урока №42


def unique_slugify(instance, slug):
    """
    Генератор уникальных SLUG в URLs для моделей, в случае существования такого SLUG.
    """
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug


def get_client_ip(request):
    """
    Get user's IP
    Функция get_client_ip() получает request и из него извлекает данные об IP адрес
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    return ip

class CkeditorCustomStorage(FileSystemStorage):
    """
    Кастомное расположение для медиа файлов редактора
    """
    def get_folder_name(self):
        return datetime.now().strftime('%Y/%m/%d')

    def get_valid_name(self, name):
        return name

    def _save(self, name, content):
        folder_name = self.get_folder_name()
        name = os.path.join(folder_name, self.get_valid_name(name))
        return super()._save(name, content)

    location = os.path.join(settings.MEDIA_ROOT, 'blog_img/')
    base_url = urljoin(settings.MEDIA_URL, 'blog_img/')


def image_compress(image_path, height, width):
    """
    Оптимизация изображений
    Ресайзинг и оптимизация изображения в Django
    не использую так как стоит другой
    """
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    if img.height > height or img.width > width:
        output_size = (height, width)
        img.thumbnail(output_size)
    img = ImageOps.exif_transpose(img)
    img.save(image_path, format='JPEG', quality=90, optimize=True)
