# Generated by Django 4.2.2 on 2023-06-22 00:44

import account.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('store', '0001_initial'),
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=16, unique=True, verbose_name='ユーザー名')),
                ('name', models.CharField(max_length=32, verbose_name='名前')),
                ('address', models.CharField(blank=True, max_length=64, verbose_name='住所')),
                ('email', models.EmailField(max_length=64, unique=True, verbose_name='メールアドレス')),
                ('register_datetime', models.DateTimeField(auto_now_add=True, verbose_name='登録日時')),
                ('is_staff', models.BooleanField(default=False, verbose_name='スタッフ')),
                ('is_active', models.BooleanField(default=True, verbose_name='有効')),
                ('cart', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.cart', verbose_name='カート')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', account.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='購入時刻')),
                ('purchase_num', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)], verbose_name='購入数')),
                ('state_flag', models.BooleanField(default=True, verbose_name='運用状況')),
                ('fk_book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='book.book', verbose_name='書籍')),
                ('fk_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
    ]
