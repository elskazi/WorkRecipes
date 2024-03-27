"""
python -m pip install Pillow
git init
pip install django-resized  Изменяет размер и качество избражения https://github.com/un1t/django-resized
pip install django-ckeditor-5
pip install django-mptt     МРТТ категории вложенные (можно одну категория вклыдвать в другую категорию)
pip install pytils          сохранения уникального slug https://proghunter.ru/articles/django-base-2023-automatic-slug-generation-cyrillic-handling-in-django-9
pip install django-debug-toolbar    INSATALL- 'debug_toolbar'  middleware - 'debug_toolbar.middleware.DebugToolbarMiddleware'
pip install django-recaptcha==3.0.0  Капча
pip install django-taggit   Тэги    py manage.py migrate
pip install django-autocomplete-light  Удалил, хотел сделать автоподстановку тегов

"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u755mln2j*cu^md5s2-_je4vnx6&o%$$=soz0!m3+-o(vkbqx+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
INTERNAL_IPS = [  # for use debug toold bar
    '127.0.0.1',
    'localhost'
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # нужен для прописывание в админке домена, дописать! SITE_ID = 1, Миграцию сделать!

    'debug_toolbar',
    'mptt',  # MPTT вложенные категории
    'django_ckeditor_5',
    'captcha',
    'taggit',

    'services',  # folder for utils

    'blog.apps.BlogConfig',  # blog
    'system.apps.SystemConfig',  # users
]
SITE_ID = 1  # нужен для прописывание в админке домена, дописать 'django.contrib.sites' и миграцию

RECAPTCHA_PUBLIC_KEY = '6LduxqUpAAAAAINXzAkfW_FO7L8vbYkDcin2Rdik'
RECAPTCHA_PRIVATE_KEY = '6LduxqUpAAAAALVRPLoJU6xPKs9w0pwccKbh_QKB'
# RECAPTCHA_DOMAIN = 'www.recaptcha.net'

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
    'debug_toolbar.middleware.DebugToolbarMiddleware'
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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
EMAIL_HOST = 'smtp.yandex.ru'  # 'mail.btrussia.ru' #'mail.btrussia.com'    'smtp.yandex.ru'
EMAIL_PORT = 465  # 25
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True  # True
EMAIL_HOST_USER = 'elskazi@yandex.ru'
EMAIL_HOST_PASSWORD = 'tasgctausctqfrnf'
EMAIL_SERVER = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = ['elskazii@yandex.ru']

# Настройки тектового редактора
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

# CKEDITOR_5_CUSTOM_CSS = 'path_to.css'                       # optional
# CKEDITOR_5_FILE_STORAGE = "path_to_storage.CustomStorage"   # optional
CKEDITOR_5_CONFIGS = {
    "default": {

        "toolbar": [
            "heading",
            "horizontalLine",
            "codeBlock",
            "htmlEmbed",
            "|",
            "outdent",
            "indent",
            "|",
            "bold",
            "italic",
            "link",
            "underline",
            "strikethrough",
            "code",
            "subscript",
            "superscript",
            "highlight",
            "|",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "blockQuote",
            "linkImage",
            "insertImage",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "mediaEmbed",
            "removeFormat",
            "insertTable",
            "sourceEditing",
            "style",
        ],
    },
    "comment": {
        "language": {"ui": "en", "content": "ar"},
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
        ],
    },
    "extends": {
        "language": "ru",
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": {
            "items": [
                "heading",
                "horizontalLine",
                "codeBlock",
                "htmlEmbed",
                "|",
                "outdent",
                "indent",
                "|",
                "bold",
                "italic",
                "link",
                "underline",
                "strikethrough",
                "code",
                "subscript",
                "superscript",
                "highlight",
                "|",
                "bulletedList",
                "numberedList",
                "todoList",
                "|",
                "blockQuote",
                "linkImage",
                "insertImage",
                "|",
                "fontSize",
                "fontFamily",
                "fontColor",
                "fontBackgroundColor",
                "mediaEmbed",
                "removeFormat",
                "insertTable",
                "sourceEditing",
                "style",
            ],
            "shouldNotGroupWhenFull": True,
        },
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
                "toggleTableCaption",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ],
        },
        "list": {
            "properties": {
                "styles": True,
                "startIndex": True,
                "reversed": True,
            },
        },
        "link": {"defaultProtocol": "https://"},
        "htmlSupport": {
            "allow": [
                {"name": "/.*/", "attributes": True, "classes": True, "styles": True},
            ],
        },
        "mention": {
            "feeds": [
                {
                    "marker": "@",
                    "feed": [
                        "@Barney",
                        "@Lily",
                        "@Marry Ann",
                        "@Marshall",
                        "@Robin",
                        "@Ted",
                    ],
                    "minimumCharacters": 1,
                },
            ],
        },
        "style": {
            "definitions": [
                {"name": "Article category", "element": "h3", "classes": ["category"]},
                {"name": "Info box", "element": "p", "classes": ["info-box"]},
            ],
        },
    },
}
