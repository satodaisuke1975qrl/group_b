from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import PermissionsMixin

# Create your models here.
# from apps.book.models import Book
from book.models import Book
from store.models import Cart


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have a email')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, cart=Cart.objects.create(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('ユーザー名', unique=True, max_length=16, )
    name = models.CharField('名前', max_length=32)
    address = models.CharField('住所', max_length=64, blank=True)
    email = models.EmailField('メールアドレス', unique=True, max_length=64)
    register_datetime = models.DateTimeField('登録日時', auto_now_add=True)
    is_staff = models.BooleanField('スタッフ', default=False)
    is_active = models.BooleanField('有効', default=True)
    cart = models.OneToOneField(to=Cart, verbose_name='カート', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [EMAIL_FIELD, 'name', 'address']

    objects = UserManager()


class Purchase(models.Model):
    fk_user = models.ForeignKey(User, verbose_name='ユーザー', on_delete=models.PROTECT)
    fk_book = models.ForeignKey(Book, verbose_name='書籍', on_delete=models.PROTECT)
    purchase_time = models.DateTimeField('購入時刻', default=timezone.now)
    purchase_num = models.PositiveIntegerField('購入数', blank=False, validators=[MaxValueValidator(10), ])
    state_flag = models.BooleanField('運用状況', default=True)

    def __str__(self):
        return str(self.fk_user) + ':' + str(self.fk_book)

class Goods(models.Model):
    name = models.CharField('商品名', unique=True, max_length=10)
    management_code = models.CharField('管理コード', unique=True, max_length=20)
    # MaxValueValidator(1000000000) 商品の価格は、10億円までしか登録できない
    price = models.PositiveIntegerField('価格', validators=[MaxValueValidator(1000000000)])
    release_date = models.DateField('発売日', blank=True, null=True)
    release_flag = models.BooleanField('発売済み', default=False)
    description = models.TextField('商品説明')
    # FileField→ファイルなんでもアップロードできるフィールド
    # ImageField→画像アップロード用のフィールド
    image = models.ImageField('商品画像', null=True, blank=True, upload_to='goods_images/')
    state_flag = models.BooleanField('運用状況', default=True)

    def __str__(self):
        return self.name
