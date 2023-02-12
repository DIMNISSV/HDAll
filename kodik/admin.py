from django.contrib import admin

from . import models


@admin.register(models.Parsed)
class ParsedAdmin(admin.ModelAdmin):
    pass
