
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tvasahi', '0022_merge_0021_alter_comment_target_0021_customuser_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー名'),
        ),
    ]
