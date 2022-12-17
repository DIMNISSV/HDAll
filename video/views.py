from django.views import generic
from django.contrib.auth import mixins

from main.mixins import BaseMixin
from . import models
from .utils import upload_to_cdn

_fields = ('to_post', 'ep_num', 's_num', 'local_file')


class UploadView(mixins.PermissionRequiredMixin, generic.CreateView, BaseMixin):
    title = 'Загрузка видео'
    permission_required = 'video.add_video'

    model = models.Video
    fields = _fields
    template_name = 'video/upload.html'


class EditView(mixins.PermissionRequiredMixin, generic.UpdateView, BaseMixin):
    title = 'Изменение видео'
    permission_required = 'video.change_video'
    model = models.Video
    fields = _fields
    template_name = 'video/upload.html'

    def form_valid(self, form):
        print(models.Video)
        old_obj = self.model.objects.get(pk=self.object.pk)
        upload_to_cdn(self.object, old_obj)
        res = super().form_valid(form)
        return res


class EmbedView(generic.DetailView, BaseMixin):
    model = models.Video
    template_name = 'video/embed.html'
