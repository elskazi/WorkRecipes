"""
git init
pip freeze > .\requirements.txt
celery -A config worker -l info  # запуск celery
celery --app=config worker --loglevel=info --pool=solo  # больше инфо

python -m pip install Pillow
pip install django-resized  Изменяет размер и качество избражения https://github.com/un1t/django-resized
pip install django-ckeditor-5
pip install django-mptt     МРТТ категории вложенные (можно одну категория вклыдвать в другую категорию)
pip install pytils          сохранения уникального slug https://proghunter.ru/articles/django-base-2023-automatic-slug-generation-cyrillic-handling-in-django-9
pip install django-debug-toolbar    INSATALL- 'debug_toolbar'  middleware - 'debug_toolbar.middleware.DebugToolbarMiddleware'
pip install django-recaptcha==3.0.0  Капча
pip install django-taggit   #Тэги    py manage.py migrate
pip install django-autocomplete-light  #Удалил, хотел сделать автоподстановку тегов
pip install psycopg2 Postgres
pip install redis  # redis-server

pip install celery  Планировзик задач
pip install django-celery-beat #компонент Celery, который отвечает за периодическое выполнение задач в фоновом режиме.

Для запуска worker'а используется команда: celery --app=config worker --loglevel=info --pool=solo
Для запуска beat'а: celery -A config beat -l info

pip install django-environ  #  корректно работали переменные виртуального окружения
"""
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

from pathlib import Path
from django.urls import reverse_lazy
from celery.schedules import crontab  # для задача резервного копирования выполнялась по расписанию
import environ  # для переменных окружения

# Работа с env.dev
env = environ.Env()
environ.Env.read_env(env_file=Path('docker/env/.env.dev'))
# параметр для правильной работы, при использовании вирт окр.
CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS').split()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# Что б проверить 404 ошибки стр надо поставить False
DEBUG = int(env('DEBUG', default=1))

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split()

# Для использования debug tool bar
INTERNAL_IPS = ['127.0.0.1', 'localhost']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # нужен для прописывание в админке домена, дописать! SITE_ID = 1, Миграцию сделать!
    'django.contrib.sitemaps',  # карта сайта, далее создаем файл в "блог" sipemap.py
    'debug_toolbar',
    'mptt',  # MPTT вложенные категории
    'django_ckeditor_5',
    'captcha',
    'taggit',
    # 'django_cleanup', #pip install django-cleanup - автоматически удалять неиспользуемые медиа-файлы

    'services',  # folder for utils

    'blog.apps.BlogConfig',  # blog
    'system.apps.SystemConfig',  # users
]

# нужен для прописывание в админке домена, дописать 'django.contrib.sites' и миграцию
SITE_ID = 1

# Капча
RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY') # '6LduxqUpAAAAAINXzAkfW_FO7L8vbYkDcin2Rdik'
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY') # '6LduxqUpAAAAALVRPLoJU6xPKs9w0pwccKbh_QKB'
# RECAPTCHA_DOMAIN = 'www.recaptcha.net'

# Тэги
TAGGIT_CASE_INSENSITIVE = True
TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'system.middleware.ActiveUserMiddleware',
    # Функционал статуса пользователя (онлайн/оффлайн) в Django с кэшированием
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'), #'WR2',
        'USER': env('POSTGRES_USER'), #'postgres',
        'PASSWORD': env('POSTGRES_PASSWORD'), #'123',
'HOST': 'localhost',
        #'HOST': env('POSTGRES_HOST'), #'localhost',
        'PORT': env('POSTGRES_PORT'), # 5432,
    }
}

# Функционал статуса пользователя (онлайн/оффлайн) в Django с кэшированием
# Кэш локаольный (в файл)
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': (BASE_DIR / 'cache'),
#     }
# }

# Кэш RedisCache ( redis-server windows)
'''
    Redis in Docker, donwload and start
    docker pull redis:latest
    docker run --name redis-server -p 6379:6379 -d redis:latest
    Если Django будет в докере то надо стучаться по адресу  redis://redis:6379 а не ЛокалХост
'''
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('REDIS_LOCATION'),
        # 'LOCATION': 'redis://localhost:6379',
    }
}

# Celery settings
CELERY_BROKER_URL = env('CELERY_BROKER_URL') #'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND') #'redis://localhost:6379/0'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'

# django-celery-beat компонент Celery, который отвечает за периодическое выполнение задач в фоновом режиме
CELERY_BEAT_SCHEDULE = {
    'backup_database': {
        'task': 'services.tasks.dbackup_task',  # Путь к задаче указанной в tasks.py
        'schedule': crontab(hour=14, minute=10),  # Резервная копия будет создаваться каждый день в полночь
    },
}

# Авторизация по email и по логину (свой бекенд аутентификации
AUTHENTICATION_BACKENDS = [
    'system.backends.UserModelBackend'
]
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

"""Подключение статики и медиа."""
STATIC_URL = 'static/'  # как быдет выглядеть ссылка
STATIC_ROOT = BASE_DIR / 'static'  # общие для всех
STATICFILES_DIRS = [  # доп папки со статикой, для отдельных приложений
    BASE_DIR / 'templates/src',
]
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = reverse_lazy("blog:news_list")  # когда вошел, куда перекинуть, обычно профайл Юзера
LOGIN_URL = reverse_lazy("blog:news_list")  # перенаправлять для ВХОДА, обычно страница Логин
LOGOUT_REDIRECT_URL = reverse_lazy("system:logout")  # ?

# Ресайз изображений при закгрузке
# https://github.com/un1t/django-resized
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_SCALE = 1
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

# YANDEX MAIL Шестерня- Все настройки - Почтовые программы - Разрешить доступ к почтовому ящику с помощью почтовых клиентов
# С сервера imap.yandex.ru по протоколу IMAP
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # для реальной отправки
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # для консоли
EMAIL_HOST = env('EMAIL_HOST') #'smtp.yandex.ru'  # 'mail.btrussia.ru' #'mail.btrussia.com'    'smtp.yandex.ru'
EMAIL_PORT = env('EMAIL_PORT') #465  # 25 foo
EMAIL_USE_TLS = int(env('EMAIL_USE_TLS', default=1))  # было False a SSL - True
#EMAIL_USE_SSL = True  # True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_SERVER = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = ['elskazii@yandex.ru']

# Настройки тектового редактора
CKEDITOR_5_FILE_STORAGE = 'services.utils.CkeditorCustomStorage'  # функция куда сохранять изобраджения именно через редактор
# CKEDITOR_5_CUSTOM_CSS = 'path_to.css'                       # optional
# CKEDITOR_5_FILE_STORAGE = "path_to_storage.CustomStorage"   # optional

customColorPalette = [
    {
        'color': 'hsl(4, 90%, 58%)',
        'label': 'Red'
    },
    {
        'color': 'hsl(340, 82%, 52%)',
        'label': 'Pink'
    },
    {
        'color': 'hsl(291, 64%, 42%)',
        'label': 'Purple'
    },
    {
        'color': 'hsl(262, 52%, 47%)',
        'label': 'Deep Purple'
    },
    {
        'color': 'hsl(231, 48%, 48%)',
        'label': 'Indigo'
    },
    {
        'color': 'hsl(207, 90%, 54%)',
        'label': 'Blue'
    },
]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],

    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
                    'code', 'subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|', 'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable', ],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side', '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells',
                               'tableProperties', 'tableCellProperties'],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'}
            ]
        }
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    }
}
