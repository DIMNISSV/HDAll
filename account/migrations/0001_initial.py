# Generated by Django 4.1.3 on 2022-11-11 12:46

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('subscribe_to', models.DateTimeField(blank=True, null=True, verbose_name='Подписка до')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('dark_theme', models.BooleanField(default=False, verbose_name='Темная тема')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ('username',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('descr', models.TextField(blank=True, max_length=300, null=True, verbose_name='Описание')),
                ('price', models.PositiveSmallIntegerField(verbose_name='Цена в ₽')),
                ('sale', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Цена в ₽ до скидки')),
                ('ad_banners_off', models.BooleanField(default=True, verbose_name='Выключить рекламу на сайте')),
                ('ad_player_off', models.BooleanField(default=True, verbose_name='Выключить рекламу в плеере')),
                ('available_sd', models.BooleanField(default=True, verbose_name='Разрешено SD')),
                ('available_hd', models.BooleanField(default=True, verbose_name='Разрешено HD')),
                ('available_fhd', models.BooleanField(default=True, verbose_name='Разрешено FHD')),
                ('available_download', models.BooleanField(default=True, verbose_name='Разрешено скачивать')),
                ('max_one_time_sessions', models.PositiveSmallIntegerField(default=3, verbose_name='Максимальное кол-во одновременных сессий')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
                'ordering': ('price',),
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('period', models.PositiveIntegerField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('subscribe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.subscribe')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]