# Generated by Django 4.2.2 on 2023-06-23 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvasahi', '0007_alter_tv_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tv',
            name='time',
            field=models.CharField(max_length=25, verbose_name='放送時間'),
        ),
    ]