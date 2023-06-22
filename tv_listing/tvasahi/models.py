from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Date(models.Model):
    on_air_date = models.CharField(verbose_name='放送日', max_length=255)

    def __str__(self):
        return self.on_air_date

    class Meta:
        verbose_name = "放送日"
        verbose_name_plural = "放送日"


class Category(models.Model):
    category_name = models.CharField('カテゴリー', max_length=255)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "カテゴリー"
        verbose_name_plural = "カテゴリー"


class Tv(models.Model):
    program_name = models.CharField('番組名', max_length=255)
    time = models.TimeField('放送時間')
    content = models.TextField('番組内容')
    url = models.URLField('番組サイト')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='カテゴリ')
    date = models.ForeignKey(Date, on_delete=models.PROTECT, verbose_name='放送日')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    class Meta:
        verbose_name = "番組タイトル"
        verbose_name_plural = "番組タイトル"


class Comment(models.Model):
    user_name = models.CharField('お名前', max_length=255, default='名無し')
    comment = models.TextField('コメント内容')
    target = models.ForeignKey(Tv, on_delete=models.PROTECT, verbose_name='紐付く番組名')

    def __str__(self):
        return self.comment[:20]

    class Meta:
        verbose_name = "コメント"
        verbose_name_plural = "コメント"


class CustomUser(AbstractUser):
    pass
