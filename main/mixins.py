from django.views.generic.base import ContextMixin


class BaseMixin(ContextMixin):
    title = 'JustWatch'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.title:
            context["page_title"] = self.title
        context['back_url'] = self.request.GET.get('back')
        return context
