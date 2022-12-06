from django.db.models import Q
from django.views.generic import ListView, FormView
from . import forms

from post import models


class SearchView(FormView, ListView):
    model = models.Post
    template_name = 'search/advanced.html'
    form_class = forms.SearchForm
    success_url = ''

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context.update({'form': self.form_class(self.request.GET)})
        return context

    def get_queryset(self):
        params = self.request.GET
        query = Q()
        try:
            con = params.get('default_condition', query.AND)
            if params.get('title'):
                query.add(
                    Q(title__icontains=params['title'])
                    | Q(rus_title__icontains=params['title'])
                    | Q(lat_title__icontains=params['title']),
                    con)
            if params.get('country'):
                for country in params['country'].split(','):
                    query.add(Q(country__icontains=country), con)
            if params.getlist('category'):
                query.add(Q(category__in=params.getlist('category')), con)
            if params.getlist('genre'):
                if params.get('genre_condition', query.OR):
                    genres = Q()
                    for genre in params.getlist('genre'):
                        genres.add(Q(genre__in=genre), params['genre_condition'])
                else:
                    genres = Q(genre__in=params.getlist('genre'))
                query.add(genres, con)
            if params.getlist('dub_workers'):
                query.add(Q(category__in=params.getlist('dub_workers')), con)
            if params.get('year'):
                years = Q()
                for year in range(*[int(i) for i in params.get('year').split('-')]):
                    years.add(Q(year__icontains=year), query.OR)
                query.add(years, con)
            if params.get('description'):
                query.add(Q(description__icontains=params['description']), con)
        except ValueError:
            pass

        return self.model.objects.filter(query)
