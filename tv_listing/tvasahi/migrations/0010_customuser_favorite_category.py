# Generated by Django 4.2.2 on 2023-06-26 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tvasahi', '0009_alter_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='favorite_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='tvasahi.category', verbose_name='好きな番組カテゴリ'),
        ),
    ]
