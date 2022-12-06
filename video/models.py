from django.db import models
from django.db.models import Q
from django.urls import reverse_lazy

from post import models as post_models
from . import utils


class Video(models.Model):
    to_post = models.ForeignKey(post_models.Post, models.CASCADE, 'video_to_post', verbose_name='Пост')
    ep_num = models.PositiveSmallIntegerField('Номер серии', default=1)
    s_num = models.PositiveSmallIntegerField('Номер сезона', default=1)
    bunny_id = models.CharField('ID на BunnyCDN', max_length=100)
    local_file = models.FileField('Локальный файл', upload_to='tmp_videos', null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.ep_num} {self.to_post} {self.s_num}'

    def get_absolute_url(self):
        return reverse_lazy('post_ep', kwargs={'slug': self.to_post.slug, 'ep_num': self.ep_num})

    def get_embed_url(self):
        return reverse_lazy('embed_video', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        obj = self.objects.filter(Q(to_post=self.to_post, ep_num=self.ep_num, s_num=self.s_num))
        if obj.exists():
            utils.upload_to_cdn(self, obj)
            obj.first().delete()
        else:
            utils.upload_to_cdn(self)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
