# Generated by Django 4.2.2 on 2023-06-28 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvasahi', '0018_alter_customuser_address_alter_customuser_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icon_images/', verbose_name='アイコン画像'),
        ),
    ]
