from django.views.generic.base import ContextMixin


class TitleMixin(ContextMixin):
    title = 'JustWatch'

    def get_context_data(self, **kwargs):
        context = {}
        if self.title:
            context["page_title"] = self.title
        context.update(kwargs)
        return super().get_context_data(**context)
