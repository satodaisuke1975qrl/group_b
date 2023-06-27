from django.views import generic
from django.views.generic.edit import ModelFormMixin

from goods.models import Goods
from store.forms import CartUnitForm


class GoodsDetail(ModelFormMixin, generic.DetailView):
    model = Goods
    template_name = 'goods/detail.html'
    context_object_name = 'goods'
    form_class = CartUnitForm

    def form_valid(self, form):
        return render(self.request, 'book/detail.html', {'form': form})
