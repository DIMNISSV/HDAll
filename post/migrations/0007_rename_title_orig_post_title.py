# Generated by Django 4.1.3 on 2023-01-05 13:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('post', '0006_rename_title_post_title_orig'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='title_orig',
            new_name='title',
        ),
    ]
