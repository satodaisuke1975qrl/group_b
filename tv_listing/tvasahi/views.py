from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from .forms import CommentCreateForm, CommentUpdateForm, SearchForm
from .models import Tv, Date


# # Create your views here.
#
#
class Home(generic.ListView):
    model = Date
    template_name = 'tvasahi/home.html'



class TvListView(generic.ListView):
    model = Tv
    template_name = 'tvasahi/tv_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        date = Date.objects.get(pk=self.kwargs['pk'])
        queryset = queryset.filter(date=date)
        return queryset


class TvDetailView(generic.DetailView):
    model = Tv
    template_name = 'tvasahi/tv_detail.html'


"""
class CommentCreateView(generic.CreateView):


class CommentListView(generic.ListView):


class CommentUpdateView(generic.UpdateView):


class CommentDeleteView(generic.DeleteView):


"""


class SearchView(generic.ListView):
    model = Tv
    template_name = 'tvasahi/tv_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # self.request.GET で値の保持が実行される
        context['form'] = SearchForm(self.request.GET)

        return context

    # 条件検索
    def get_queryset(self):

        queryset = super().get_queryset()
        form = SearchForm(self.request.GET)
        form.is_valid()

        keyword = form.cleaned_data.get('keyword')
        category = form.cleaned_data.get('category')

        if keyword:
            queryset = queryset.filter(
                Q(program_name__icontains=keyword) | Q(content__icontains=keyword)
            )

        if category:
            queryset = queryset.filter(category=category)

        return queryset