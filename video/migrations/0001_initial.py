# Generated by Django 4.1.3 on 2022-11-11 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ep_num', models.PositiveSmallIntegerField(default=1, verbose_name='Номер серии')),
                ('s_num', models.PositiveSmallIntegerField(default=1, verbose_name='Номер сезона')),
                ('bunny_id', models.CharField(max_length=100, verbose_name='ID на BunnyCDN')),
                ('local_file', models.FileField(blank=True, null=True, upload_to='tmp_videos', verbose_name='Локальный файл')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('to_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_to_post', to='post.post', verbose_name='Пост')),
            ],
        ),
    ]
