# Generated by Django 4.2.2 on 2023-06-27 01:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tvasahi', '0012_comment_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー名'),
        ),
    ]