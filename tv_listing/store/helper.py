from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Goods

class OnlyYouMixin(UserPassesTestMixin):
    login_url = 'account:login'

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk']


class GetOnlyYouMixin(UserPassesTestMixin):
    '''
    urlにpkが入らない場合はこちらをつかう
    '''
    login_url = 'account:login'

    def test_func(self):
        request_user = self.request.user
        cart_user = self.request.GET.get('uname', False)
        return request_user.username == cart_user


class PostOnlyYouMixin(UserPassesTestMixin):
    login_url = 'account:login'

    def test_func(self):
        request_user = self.request.user
        cart_user = self.request.POST.get('uname', False)
        return request_user.username == cart_user


class SessionCartManager:
    """
    Session Cartの構造: [{'goods_pk':foo, 'quantity': bar }, {}, ・・・]
    """
    kname = 'cart'  # key name

    @staticmethod
    def _make_unit(goods_pk, quantity=1):
        return {'goods_pk': int(goods_pk), 'quantity': int(quantity)}

    @staticmethod
    def add_unit(lis_cart, goods_pk, quantity=1):
        goods_pk = int(goods_pk)
        quantity = int(quantity)
        for cart_unit in lis_cart:
            if cart_unit['goods_pk'] == int(goods_pk):
                cart_unit['quantity'] += quantity
                return lis_cart
        lis_cart.append(SessionCartManager._make_unit(goods_pk, quantity))
        return lis_cart

    @staticmethod
    def delete_unit(lis_cart, goods_pk):
        goods_pk = int(goods_pk)
        for cart_unit in lis_cart:
            if cart_unit['goods_pk'] == goods_pk:
                lis_cart.remove(cart_unit)
        return lis_cart

    @staticmethod
    def to_rendered(lis_cart):
        """
        templateが必要とする情報にフォーマットする。（このメソッドが返すものをコンテキストに追加すればよい）
        """
        return [{'goods':Goods.objects.get(pk=cart_unit['goods_pk']).title,
                 'quantity': cart_unit['quantity'],
                 'goods_pk': cart_unit['goods_pk']}
                for cart_unit in lis_cart]
