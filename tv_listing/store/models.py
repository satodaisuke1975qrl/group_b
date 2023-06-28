
from django.core.validators import MinValueValidator
from tvasahi.models import CustomUser
from django.utils import timezone
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


class CartUnit(models.Model):
    """Cartに格納される最小単位"""
    goods = models.ForeignKey(to=Goods, verbose_name='書籍', on_delete=models.CASCADE, blank=False)
    quantity = models.PositiveIntegerField('購入数', default=1, blank=False, validators=[MinValueValidator(1, )])

    def __str__(self):
        return '{}:{}'.format(self.goods.name, self.quantity)


class Cart(models.Model):
    units = models.ManyToManyField(to=CartUnit, verbose_name=' ユニット', blank=True)

    @property
    def total_price(self):
        """:returns total price of goodss in a cart"""
        each_goodss_price = [unit.goods.price * unit.quantity for unit in self.units.all()]
        return sum(each_goodss_price)

    def add_unit(self, unit_add):
        """CartUnitをカートに追加する際に呼び出す。
        既に同じ種類の本がカートに存在する際は、個数を足し算するようにする。
        """
        if unit_add.goods in [unit.goods for unit in self.units.all()]:
            unit_origin = self.units.get(goods_id=unit_add.goods.id)
            unit_origin.quantity += unit_add.quantity
            unit_origin.save()
        else:
            unit_add.save()
            self.units.add(unit_add)

    def _add_session_unit(self, goods_pk, quantity):
        """Session CartのカートユニットをModel CartのCartUnitに変換した上で、追加する。
        既に同じ種類の本がカートに存在する際は、個数を足し算するようにする。
        """
        goods_pk = int(goods_pk)
        if goods_pk in [unit.goods.pk for unit in self.units.all()]:
            unit_origin = self.units.get(goods_id=goods_pk)
            unit_origin.quantity += quantity
            unit_origin.save()
        else:
            unit_add = CartUnit(goods=Goods.objects.get(pk=goods_pk), quantity=quantity)
            unit_add.save()
            self.units.add(unit_add)

    def import_session(self, session_cart):
        """Session Cartの中身をすべてモデルカートに移す"""
        for cart_unit in session_cart:
            self._add_session_unit(cart_unit['goods_pk'], cart_unit['quantity'])

    def __str__(self):
        print(self.customuser)
        if hasattr(self, 'customuser'):
            return "{}'s model cart".format(self.customuser.username)

        else:
            return 'まだ紐づいていません'



class Purchase(models.Model):
    fk_user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    fk_goods = models.ForeignKey(Goods, verbose_name='書籍', on_delete=models.PROTECT)
    purchase_time = models.DateTimeField('購入時刻', default=timezone.now)
    purchase_num = models.PositiveIntegerField('購入数', blank=False, validators=[MaxValueValidator(10), ])
    state_flag = models.BooleanField('運用状況', default=True)

    def __str__(self):
        return str(self.fk_user) + ':' + str(self.fk_goods)
