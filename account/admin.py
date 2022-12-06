from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class MyUserAdmin(UserAdmin):
    model = models.User
    _fields = ('Данные', {'fields': ('birth_date', 'dark_theme', 'subscribe', 'subscribe_to')})
    add_fieldsets = (
        *UserAdmin.add_fieldsets, _fields
    )
    fieldsets = (
        *UserAdmin.fieldsets, _fields
    )


@admin.register(models.Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
