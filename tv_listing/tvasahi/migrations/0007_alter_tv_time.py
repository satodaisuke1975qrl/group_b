# Generated by Django 4.2.2 on 2023-06-23 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvasahi', '0006_alter_tv_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tv',
            name='time',
            field=models.TimeField(default='00:00', verbose_name='放送時間'),
        ),
    ]
