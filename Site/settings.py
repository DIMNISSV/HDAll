from pathlib import Path
from .secret_params import *

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'hdall.ru', 'hdall.store']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'post.apps.PostConfig',
    'account.apps.AccountConfig',
    'main.apps.MainConfig',
    'video.apps.VideoConfig',
    'kodik.apps.KodikConfig',
    'search.apps.SearchConfig',
    'order_table.apps.OrderTableConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'Site.wsgi.application'

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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / r'cache',
    }
}

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = ['static']
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGOUT_REDIRECT_URL = 'login'
AUTH_USER_MODEL = 'account.User'
LOGIN_REDIRECT_URL = 'my_profile'
LOGIN_URL = 'login'
X_FRAME_OPTIONS = 'SAMEORIGIN'

KODIK_MODEL = 'post.models.Post'
KODIK_FIELDS = {'title': 'rus_title',
                'title_orig': 'title_orig',
                'worldart_link': 'wa_link',
                'type': 'category',
                'translation': 'dub_workers',
                'last_season': 'season_total',
                'last_episode': 'episode',
                'episodes_count': 'episode_total',
                'material_data.poster_url': 'poster',
                'material_data.description': 'description',
                'material_data.all_genres': 'genre'
                }
KODIK_ONENAME_FIELDS = ('year', 'kinopoisk_id', 'imdb_id', 'mdl_id', 'shikimori_id')
TYPE_TO_CATEGORY = {'foreign-movie': 'Зарубежный фильм',
                    'soviet-cartoon': 'Советский мультик',
                    'foreign-cartoon': 'Зарубежный мультик',
                    'russian-cartoon': 'Русский мультик',
                    'anime': 'Аниме',
                    'russian-movie': 'Русский фильм',
                    'cartoon-serial': 'Мультсериал',
                    'documentary-serial': 'Документальный сериал',
                    'russian-serial': 'Русский сериал',
                    'foreign-serial': 'Зарубежный сериал',
                    'anime-serial': 'Аниме сериал',
                    'multi-part-film': 'Многосерийный фильм'}
KODIK_M2M_FIELDS = {'category', 'genre', 'persons', 'dub_workers'}
KODIK_ID_FIELDS = {'title_orig', 'kinopoisk_id', 'imdb_id', 'shikimori_id', 'mdl_id', 'wa_link'}
