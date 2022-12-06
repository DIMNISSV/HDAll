from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import SET_NULL
from django.urls import reverse_lazy
from post import models as post
from Site import settings


class Subscribe(models.Model):
    title = models.CharField('Название', max_length=100, unique=True)
    descr = models.TextField('Описание', max_length=300, blank=True, null=True)
    price = models.PositiveSmallIntegerField('Цена в ₽')
    sale = models.PositiveSmallIntegerField('Цена в ₽ до скидки', null=True, blank=True)
    ad_banners_off = models.BooleanField('Выключить рекламу на сайте', default=True)
    ad_player_off = models.BooleanField('Выключить рекламу в плеере', default=True)
    available_sd = models.BooleanField('Разрешено SD', default=True)
    available_hd = models.BooleanField('Разрешено HD', default=True)
    available_fhd = models.BooleanField('Разрешено FHD', default=True)
    available_download = models.BooleanField('Разрешено скачивать', default=True)
    max_one_time_sessions = models.PositiveSmallIntegerField('Максимальное кол-во одновременных сессий', default=3)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('price',)

    def __str__(self):
        return self.title


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, SET_NULL, null=True)
    amount = models.FloatField()
    period = models.PositiveIntegerField()
    subscribe = models.ForeignKey(Subscribe, SET_NULL, null=True)
    time = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    subscribe = models.ForeignKey(Subscribe, SET_NULL, verbose_name='Подписка', null=True)
    subscribe_to = models.DateTimeField('Подписка до', blank=True, null=True)

    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    dark_theme = models.BooleanField('Темная тема', default=False)
    favorite_posts = models.ManyToManyField(post.Post, blank=True)
    favorite_categories = models.ManyToManyField(post.Category, blank=True)
    favorite_genres = models.ManyToManyField(post.Genre, blank=True)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_absolute_url(self):
        return reverse_lazy('profile', kwargs={'username': self.username})
