from django.db import models
from django.urls import reverse_lazy


class Order(models.Model):
    title_orig = models.CharField('Оригинальное название', max_length=300)
    kinopoisk_id = models.CharField('ID KinoPoisk', max_length=32, blank=True, null=True)
    imdb_id = models.CharField('ID IMDB', max_length=32, blank=True, null=True)
    shikimori_id = models.CharField('ID Shikimory', max_length=200, blank=True, null=True)
    worldart_link = models.URLField('Ссылка на World-Art', max_length=32, blank=True, null=True)
    mdl_id = models.CharField('ID MyDoramaList', max_length=200, blank=True, null=True)
    comment = models.TextField('Комментарий для модератора', blank=True, null=True)

    @staticmethod
    def get_absolute_url():
        return reverse_lazy('order')
