from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    pass
