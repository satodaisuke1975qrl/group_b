from django.shortcuts import render, redirect, resolve_url
from django.views import generic
from django.urls import reverse_lazy
from .forms import CommentCreateForm, CommentUpdateForm, SearchForm, CustomUserCreationForm, UserUpdateForm
from .models import Tv, Date, Comment, CustomUser
from django.db.models import Q

# ログインとログアウト
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView

# マイページ
from django.contrib.auth import get_user_model, logout, login, authenticate  # 追加
from django.contrib.auth.mixins import UserPassesTestMixin  # 追加
from django.contrib import messages


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


def a(obj):
    hour_and_minits = obj.time.split(':')
    hour = hour_and_minits[0]
    minits = hour_and_minits[1]
    return int(hour), int(minits)


class TvListView(generic.ListView):
    model = Tv
    template_name = 'tvasahi/tv_list.html'

    def get_context_data(self):
        context = {}
        queryset = Tv.objects.all()
        date = Date.objects.get(pk=self.kwargs['pk'])
        queryset = queryset.filter(date=date)
        queryset = list(queryset)
        # 昇順
        queryset.sort(key=a)
        # 降順
        # queryset.sort(key=a, reverse=True)
        context['tv_list'] = queryset

        date_list = Date.objects.all()
        context['date_list'] = date_list

        return context


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
        comment.user_name = self.request.user

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

"""


# class CommentDeleteView(generic.DeleteView):
#     model = Comment
#     success_url = reverse_lazy('tvasahi:tv_detail')
#
#     def get_success_url(self):
#         return resolve_url('tvasahi:tv_detail', pk=self.kwargs['pk'])

class CommentDeleteView(generic.DeleteView):
    model = Comment
    success_url = reverse_lazy('tvasahi:tv_detail')

    def get_success_url(self):
        return resolve_url('tvasahi:tv_detail', self.object.target.pk)




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

    def get(self, request):
        logout(request)
        messages.success(request, 'ログアウトしました。')
        return redirect('tvasahi:home')


class CustomUserCreationView(generic.CreateView):
    Model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'tvasahi/user_create.html'
    success_url = reverse_lazy('tvasahi:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


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


class UserUpdate(OnlyYouMixin, generic.UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'tvasahi/user_update.html'

    def get_success_url(self):
        return resolve_url('tvasahi:mypage', pk=self.kwargs['pk'])


class CustomUserDeleteView(generic.DeleteView):
    template_name = 'tvasahi/user_delete.html'
    model = CustomUser
    success_url = reverse_lazy('tvasahi:home')
