from django import forms
from post import models


class SearchForm(forms.ModelForm):
    title = forms.CharField(label='Название', required=False)
    default_condition = forms.ChoiceField(choices=(('AND', 'И'), ('ОR', 'ИЛИ')), label='Как соединять параметры поиска',
                                          required=False)
    genre_condition = forms.ChoiceField(
        choices=(('ОR', 'Любой из жанров присутствует'), ('AND', 'Все жанры присутствуют')),
        label='Условие для жанров', required=False)

    class Meta:
        model = models.Post
        fields = ['category', 'genre', 'country', 'year', 'dub_workers', 'description']
