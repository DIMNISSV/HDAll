# Generated by Django 4.1.3 on 2022-11-11 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orig_title', models.CharField(max_length=300, verbose_name='Оригинальное название')),
                ('kinopoisk_id', models.CharField(blank=True, max_length=32, null=True, verbose_name='ID KinoPoisk')),
                ('imdb_id', models.CharField(blank=True, max_length=32, null=True, verbose_name='ID IMDB')),
                ('shikimori_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='ID Shikimory')),
                ('worldart_link', models.URLField(blank=True, max_length=32, null=True, verbose_name='Ссылка на World-Art')),
                ('mdl_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='ID MyDoramaList')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий для модератора')),
            ],
        ),
    ]