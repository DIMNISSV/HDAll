from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic

from main.mixins import TitleMixin
from video.models import Video
from . import models, utils


class AllView(generic.ListView, TitleMixin):
    title = 'Все публикации'
    template_name = 'post/all.html'
    model = models.Post
    extra_context = {'title': 'Все публикации'}


class PostDetail(generic.DetailView, TitleMixin):
    template_name = 'post/detail.html'
    model = models.Post

    def get_context_data(self, **kwargs):
        self.title = self.object.rus_title
        context_data = super().get_context_data(**kwargs)

        kodik_list = utils.get_kodik_list(self.object)
        our_list = utils.get_video_list(self.object, Video)

        translate = self.kwargs.get('translate', list(kodik_list.keys())[0])
        kodik_episode_list = sorted(kodik_list.get(translate))
        context_data['translate'] = translate
        context_data['ep_num'] = self.kwargs.get('ep_num', 1)
        context_data['kodik_translate_list'] = kodik_list.keys()
        context_data['kodik_episode_list'] = enumerate(kodik_episode_list, 1)
        context_data['current_video'] = our_list.get(context_data['ep_num'])
        if 0 < context_data['ep_num'] <= len(kodik_episode_list):
            context_data['kodik_video'] = kodik_episode_list[context_data['ep_num'] - 1]

        return context_data


class PostEditView(PermissionRequiredMixin, generic.UpdateView, TitleMixin):
    permission_required = 'post.change_post'
    template_name = 'post/edit.html'
    model = models.Post
    fields = '__all__'

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        self.title = f'Редактирование {obj.rus_title}'
        return obj


class PostAddView(PermissionRequiredMixin, generic.CreateView, TitleMixin):
    title = 'Добавление публикации'
    permission_required = 'post.add_post'
    template_name = 'post/add.html'
    model = models.Post
    fields = '__all__'
