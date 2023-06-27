from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class Goods(models.Model):
    name = models.CharField('商品名', unique=True, max_length=100)
    price = models.PositiveIntegerField('価格', validators=[MaxValueValidator(1000000000)])
    description = models.TextField('商品説明')
    # FileField→ファイルなんでもアップロードできるフィールド
    # ImageField→画像アップロード用のフィールド
    image = models.ImageField('商品画像', null=True, blank=True, upload_to='goods_images/')

    def __str__(self):
        return self.name