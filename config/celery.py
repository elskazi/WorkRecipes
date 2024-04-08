# https://proghunter.ru/articles/django-base-2023-installing-redis-and-celery-for-asynchronous-tasks
'''

Здесь мы указываем, что настройки для Celery мы будем брать из namespace 'CELERY' в settings.py.
Также мы автоматически ищем файлы tasks.py во всех приложениях Django, которые используют Celery.

Далее нам необходимо добавить обработку Celery в файл init.py, который находится также в папке backend.
'''

import os

from celery import Celery

# Установите модуль настроек Django по умолчанию для программы «Celery».
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()