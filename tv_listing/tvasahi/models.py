from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings


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
    time = models.CharField('放送時間', max_length=25)
    content = models.TextField('番組内容')
    url = models.URLField('番組サイト', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='カテゴリ')
    date = models.ForeignKey(Date, on_delete=models.PROTECT, verbose_name='放送日')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def get_time_hour_and_minute(self):
        return self.time[:5]

    class Meta:
        verbose_name = "番組タイトル"
        verbose_name_plural = "番組タイトル"

    def __str__(self):
        return self.program_name


class Comment(models.Model):
    user_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ユーザー名')
    comment = models.TextField('コメント内容')
    # target = models.ForeignKey(Tv, on_delete=models.PROTECT, verbose_name='紐付く番組名')
    target = models.ForeignKey(Tv, on_delete=models.CASCADE, verbose_name='紐付く番組名')
    # 登録日時
    pub_date = models.DateTimeField('登録日時', auto_now_add=True)

    def __str__(self):
        return self.comment[:20]

    class Meta:
        verbose_name = "コメント"
        verbose_name_plural = "コメント"


class CustomUser(AbstractUser):
    icon = models.ImageField('アイコン画像', null=True, blank=True, upload_to='icon_images/')
    email = models.EmailField('メールアドレス', unique=True)
    address = models.CharField('住所', max_length=64, blank=False, null=False)
    favorite_category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='好きな番組カテゴリ', null=True)
    cart = models.OneToOneField(to='store.Cart', verbose_name='カート', on_delete=models.CASCADE, blank=True, null=True)

