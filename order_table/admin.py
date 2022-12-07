from django.contrib import admin

from . import models


@admin.register(models.Order)
class SubscribeAdmin(admin.ModelAdmin):
    pass
