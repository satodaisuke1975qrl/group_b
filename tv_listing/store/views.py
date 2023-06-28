
from .forms import GoodsSearchForm, CartUnitForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .helper import OnlyYouMixin, PostOnlyYouMixin, GetOnlyYouMixin, PostOnlyYouMixin, SessionCartManager
from tvasahi.models import CustomUser
from .models import Goods, CartUnit, Purchase
from django import forms
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.generic.edit import ModelFormMixin
from .models import Cart


class Home(generic.ListView):
    model = Goods
    template_name = 'store/home.html'
    form_class = GoodsSearchForm
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(generic.ListView, self).get_context_data(**kwargs)
        context.update(dict(form=self.form_class, query_string=self.request.GET.urlencode()))

        q_title = self.request.GET.get('title')

        context['form'] = GoodsSearchForm(initial={
            'title': q_title,})

        return context

    def get_queryset(self):
        goodss = Goods.objects.all()
        q_title = self.request.GET.get('title')

        if q_title:
            goodss = goodss.filter(title__icontains=q_title)

        return goodss


@method_decorator(never_cache, name='dispatch')
class ModelCartContent(OnlyYouMixin, generic.DetailView):
    model = CustomUser
    context_object_name = 'cart'
    template_name = 'store/contents.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj.cart


class ModelAddToCart(LoginRequiredMixin, generic.RedirectView):
    """CartUnitをカートに追加する。
    どのユーザのカートの追加するかは、サーバ側で決定しているので、OnlyYouMixinはいらない
    """

    def get_redirect_url(self):
        user_pk = self.request.user.pk
        return reverse_lazy('store:modelcart_content', args=(user_pk,))

    def post(self, request, *args, **kwargs):
        user = request.user

        if not user.cart:
            user.cart = Cart.objects.create()
            user.save()

        goods_pk = request.POST['goods_pk']
        quantity = request.POST['quantity']
        user.cart.add_unit(CartUnit(goods=Goods.objects.get(pk=goods_pk), quantity=int(quantity)))
        return super().post(request, *args, **kwargs)


class ModelCartDelete(PostOnlyYouMixin, generic.DeleteView):
    """
    CartUnitをカートに追加する。
    """
    model = CartUnit

    def get_object(self, queryset=None):
        unit_pk = self.request.POST['unit_pk']
        return CartUnit.objects.get(id=unit_pk)

    def get_success_url(self):
        user_pk = self.request.user.pk
        return reverse_lazy('store:modelcart_content', args=(user_pk,))


@method_decorator(never_cache, name='dispatch')
class PurchasePreview(GetOnlyYouMixin, generic.TemplateView):
    template_name = 'store/preview.html'

    def get_context_data(self, **kwargs):
        cart = self.request.user.cart
        ctx = super().get_context_data(**kwargs)
        ctx['total_price'] = cart.total_price
        return ctx


@method_decorator(never_cache, name='dispatch')
class PurchaseProcess(PostOnlyYouMixin, generic.FormView):
    """
    TemplateView ではpostは未実装。
    djangoのformは使わない
    """
    form_class = forms.Form
    success_url = reverse_lazy('store:purchase_done')

    def form_valid(self, form):
        user = self.request.user

        for unit in user.cart.units.all():
            Purchase.objects.create(fk_user=user, fk_goods=unit.goods, purchase_num=unit.quantity)
        user.cart.units.clear()
        return super().form_valid(form)


class PurchaseDone(generic.TemplateView):
    template_name = 'store/done.html'


@method_decorator(never_cache, name='dispatch')
class SessionCartContent(generic.TemplateView):
    template_name = 'store/contents.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        cart = self.request.session.get(SessionCartManager.kname, [])
        ctx['lis_cart'] = SessionCartManager.to_rendered(cart)
        return ctx


class SessionAddToCart(generic.RedirectView):
    url = reverse_lazy('store:sessioncart_content')

    def post(self, request, *args, **kwargs):
        goods_pk = request.POST['goods_pk']
        quantity = request.POST['quantity']
        cart = request.session.get(SessionCartManager.kname, [])
        cart = SessionCartManager.add_unit(cart, goods_pk, quantity)
        request.session[SessionCartManager.kname] = cart
        return super().post(request, *args, **kwargs)


class SessionCartDelete(generic.FormView):
    form_class = forms.Form
    success_url = reverse_lazy('store:sessioncart_content')

    def form_valid(self, form):
        cart = self.request.session[SessionCartManager.kname]
        deleting_goods_pk = int(self.request.POST['goods_pk'])
        cart = SessionCartManager.delete_unit(cart, deleting_goods_pk)
        self.request.session[SessionCartManager.kname] = cart
        return super().form_valid(form)


class GoodsDetail(ModelFormMixin, generic.DetailView):
    model = Goods
    template_name = 'store/detail.html'
    context_object_name = 'goods'
    form_class = CartUnitForm

    def form_valid(self, form):
        return render(self.request, 'store/detail.html', {'form': form})
