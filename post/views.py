from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views import generic

from main.mixins import BaseMixin, UserParamsMixin
from video.models import Video
from . import models, utils


class AllView(UserParamsMixin, generic.ListView, BaseMixin):
    title = 'Все публикации'
    template_name = 'post/all.html'
    model = models.Post
    extra_context = {'title': 'Все публикации'}


class PostDetail(generic.DetailView, BaseMixin):
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
        if len(kodik_episode_list) <= 1:
            context_data['is_movie'] = True
        context_data['kodik_episode_list'] = enumerate(kodik_episode_list, 1)
        context_data['current_video'] = our_list.get(context_data['ep_num'])
        if 0 < context_data['ep_num'] <= len(kodik_episode_list):
            context_data['kodik_video'] = kodik_episode_list[context_data['ep_num'] - 1]
        context_data['player'] = 'kodik'
        return context_data


class PostEditView(PermissionRequiredMixin, generic.UpdateView, BaseMixin):
    permission_required = 'post.change_post'
    template_name = 'post/edit.html'
    model = models.Post
    fields = '__all__'

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        self.title = f'Редактирование {obj.rus_title}'
        return obj


class PostAddView(PermissionRequiredMixin, generic.CreateView, BaseMixin):
    title = 'Добавление публикации'
    permission_required = 'post.add_post'
    template_name = 'post/add.html'
    model = models.Post
    fields = '__all__'


@login_required
def vote_view(request, pk):
    obj = models.Post.objects.get(pk=pk)
    voted = models.Vote.objects.filter(user=request.user)
    rating = int(request.GET.get('rating', 0))
    if obj:
        if voted:
            voted[0].value = rating
        else:
            voted = models.Vote(user=request.user, post=obj, value=rating)
        voted[0].save()
    return redirect(request.headers.get('referer', 'main_page'))
