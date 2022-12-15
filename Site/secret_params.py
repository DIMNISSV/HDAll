FREEKASSA_M = 23141
FREEKASSA_SECRET = 'gVWh.2$}eDe%i=*'
FREEKASSA_CURRENCY = 'RUB'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'justwatching',
        'USER': 'justwatch_user',
        'PASSWORD': '123',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}