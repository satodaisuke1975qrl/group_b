# Generated by Django 4.2.2 on 2023-06-22 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='カテゴリー名')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='書籍名')),
                ('price', models.PositiveIntegerField(verbose_name='価格')),
                ('description', models.TextField(max_length=500, verbose_name='説明')),
                ('fk_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.category', verbose_name='カテゴリー')),
            ],
        ),
    ]
