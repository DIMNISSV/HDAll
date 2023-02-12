from django.db import models


class Parsed(models.Model):
    next_page = models.CharField('Следующая страница', max_length=100)
    page = models.CharField('Последняя спаршенная страница', max_length=100)
    all_have = models.BooleanField('Все с этой стр. уже добавленны', default=False)

    def __str__(self):
        return self.page
