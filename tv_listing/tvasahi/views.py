from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from .forms import CommentCreateForm, CommentUpdateForm, SearchForm, CustomUserCreationForm
from .models import Tv, Date, Comment, CustomUser
from django.db.models import Q

# ログインとログアウト
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView

# マイページ
from django.contrib.auth import get_user_model  # 追加
from django.contrib.auth.mixins import UserPassesTestMixin  # 追加


# # Create your views here.
#
#
class Home(generic.ListView):
    model = Date
    template_name = 'tvasahi/home.html'

    def get_context_data(self):
        context = super().get_context_data()
        date = Date.objects.get(on_air_date='6/30')
        tv_list = Tv.objects.filter(date=date)
        context['tv_list'] = tv_list
        return context


class TvListView(generic.ListView):
    model = Tv
    template_name = 'tvasahi/tv_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        date = Date.objects.get(pk=self.kwargs['pk'])
        queryset = queryset.filter(date=date)
        return queryset


class TvListHomeView(generic.ListView):
    model = Tv
    template_name = 'tvasahi/home.html'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     date = Date.objects.get(pk=self.kwargs['pk'])
    #     queryset = queryset.filter(date=date)
    #     return queryset


class TvDetailView(generic.DetailView):
    model = Tv
    template_name = 'tvasahi/tv_detail.html'


class CommentCreateView(generic.CreateView):
    model = Comment
    template_name = 'tvasahi/comment_create.html'
    form_class = CommentCreateForm
    success_url = reverse_lazy('tvasahi:tv_detail')

    def form_valid(self, form):
        # form.save(commit=False) データベースにはまだ保存しない
        # commit=False　ビューでモデルのフィールドを埋めるために使う引数
        comment = form.save(commit=False)

        # commentモデルのtargetフィールドをここで埋める
        # モデル名.objects.get(フィールド=値) 1つだけDBから取り出すのに使うメソッドがget
        # url内の<int:pk>はself.kwargs['pk']で取得できる
        comment.target = Tv.objects.get(pk=self.kwargs['pk'])

        # 上2行をまとめてこう書かれている場合も多い
        # form.instance.target = Article.objects.get(pk=self.kwargs['pk'])

        comment.save()
        return redirect('tvasahi:tv_detail', self.kwargs['pk'])


"""
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


class Login(LoginView):
    template_name = 'tvasahi/login.html'


class Logout(LogoutView):
    template_name = 'tvasahi/logout.html'


class CustomUserCreationView(generic.CreateView):
    Model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'tvasahi/user_create.html'
    success_url = reverse_lazy('tvasahi:home')


# 自分しかアクセスできないようにする
class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # 今ログインしてるユーザーのpkと、そのマイページのpkが同じなら許可
        user = self.request.user
        return user.pk == self.kwargs['pk']


# マイページ
class MyPage(OnlyYouMixin, generic.DetailView):
    model = CustomUser
    template_name = 'tvasahi/mypage.html'
    # モデル名小文字(user)でモデルインスタンスがテンプレートファイルに渡される
