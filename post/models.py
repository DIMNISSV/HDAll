from pathlib import Path

from django.db import models
from django.db.models import CASCADE, Q
from django.urls import reverse_lazy

from Site import settings
from . import utils


class Category(models.Model):
    title = models.CharField('Название', max_length=100)
    slug = models.CharField('Ссылка', max_length=100, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('login')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    title = models.CharField('Название', max_length=100)
    slug = models.SlugField('Ссылка', max_length=100, unique=True)
    description = models.TextField('Описание', max_length=300, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Person(models.Model):
    name = models.CharField('Имя', max_length=100)
    page = models.URLField('Ссылка на личную страницу', blank=True, null=True)
    description = models.TextField('Описание', max_length=400, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'


class DubWorker(models.Model):
    _jobs = (('dubber', 'даббер'), ('sounder', 'технарь'), ('translator', 'переводчик'), ('team', 'команда'))
    title = models.CharField('Имя', max_length=100)
    page = models.URLField('Ссылка на страницу', blank=True, null=True)
    job = models.CharField('Тип', max_length=10, choices=_jobs)
    description = models.TextField('Описание', max_length=400, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Работающий над озвучками'
        verbose_name_plural = 'Работающие над озвучками'


class Post(models.Model):
    title_orig = models.CharField('Оригинальное название', max_length=200)
    slug = models.SlugField('Ссылка', max_length=200, unique=True)
    rus_title = models.CharField('Название на русском', max_length=200, blank=True, null=True)
    lat_title = models.CharField('Оригинальное название на латинице', max_length=200, blank=True, null=True)
    description = models.TextField('Описание', max_length=1200, blank=True, null=True)
    poster = models.ImageField('Постер', upload_to='posters', blank=True, null=True)
    category = models.ManyToManyField(Category, verbose_name='Категория', blank=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр', blank=True)
    year = models.CharField('Год', max_length=9, blank=True, null=True, validators=[utils.validate_year])
    country = models.CharField('Страна', max_length=100, blank=True, null=True)
    kinopoisk_id = models.CharField('ID KinoPoisk', max_length=32, blank=True, null=True)
    imdb_id = models.CharField('ID IMDB', max_length=32, blank=True, null=True)
    shikimori_id = models.CharField('ID Shikimory', max_length=200, blank=True, null=True)
    wa_link = models.URLField('Ссылка на World-Art', blank=True, null=True)
    mdl_id = models.CharField('ID MyDoramaList', max_length=200, blank=True, null=True)
    season_total = models.PositiveSmallIntegerField('Всего сезонов', blank=True, null=True)
    season = models.PositiveSmallIntegerField('Вышло сезонов', blank=True, null=True)
    episode_total = models.PositiveSmallIntegerField('Всего серий', blank=True, null=True)
    episode = models.PositiveSmallIntegerField('Вышло серий', blank=True, null=True)
    persons = models.ManyToManyField(Person, verbose_name='Люди работающие над этим', blank=True)
    dub_workers = models.ManyToManyField(DubWorker, verbose_name='Люди работающие над озвучкой', blank=True)
    updated_at = models.DateTimeField('Последнее обновление', auto_now=True)

    def __str__(self):
        return self.title_orig

    def save(self, *args, **kwargs):
        if self.poster and Path(self.poster.name).suffix != '.webp':
            old_path = self.poster.path
            self.poster.save(Path(self.poster.name).with_suffix('.webp').name, self.poster.file)
            utils.convert_img(self.poster, old_path)
        if not self.slug:
            self.slug = utils.gen_slug(self)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        url = reverse_lazy('post_slug', kwargs={'slug': self.slug}) if self.slug \
            else reverse_lazy('post_pk', kwargs={'pk': self.pk})
        return url

    def get_rating(self):
        to_this = Vote.objects.filter(post=self)
        return sum(*to_this.values_list('value'), ) / (to_this.count() or 1)

    @staticmethod
    def check_exist(**kwargs):
        params = Q()
        ids = [(name, kwargs[name]) for name in
               settings.KODIK_ID_FIELDS if name in kwargs and
               kwargs[name]]
        for name, value in ids:
            params.add(Q(**{name: value}), params.AND)

        other = Post.objects.filter(params)
        if len(other) > 0:
            obj = other[0]
            for k, v in kwargs.items():
                if hasattr(obj, k) and getattr(obj, k) != v:
                    if k in settings.KODIK_M2M_FIELDS:
                        getattr(obj, k).clear()
                        for i in v:
                            if hasattr(i, 'pk'):
                                getattr(obj, k).add(i.pk)
                    setattr(obj, k, v)
            return obj
        obj = Post()
        for k, v in kwargs.items():
            if k not in settings.KODIK_M2M_FIELDS:
                setattr(obj, k, v)
        return obj

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-updated_at',)


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    post = models.ForeignKey(Post, models.CASCADE)
    value = models.FloatField()


class Comment(models.Model):
    post = models.ForeignKey(Post, CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, CASCADE)
    text = models.TextField('Текст', max_length=400)

    def __str__(self):
        return f'{self.post} [{self.user}]'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
