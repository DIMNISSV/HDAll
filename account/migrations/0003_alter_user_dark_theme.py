# Generated by Django 4.1.3 on 2022-12-28 12:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dark_theme',
            field=models.BooleanField(default=True, verbose_name='Темная тема'),
        ),
    ]
