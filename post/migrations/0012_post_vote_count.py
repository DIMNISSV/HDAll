# Generated by Django 4.1.3 on 2023-01-15 05:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('post', '0011_alter_post_options_post_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='vote_count',
            field=models.IntegerField(default=0, verbose_name='Кол-во проголосовавших'),
        ),
    ]
