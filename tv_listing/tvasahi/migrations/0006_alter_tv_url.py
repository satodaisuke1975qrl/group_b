# Generated by Django 4.2.2 on 2023-06-22 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvasahi', '0005_alter_tv_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tv',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='番組サイト'),
        ),
    ]
