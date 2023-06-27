from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'tvasahi'

urlpatterns = [
    path('home/', views.Home.as_view(), name='home'),
    path('tvlist/<int:pk>/', views.TvListView.as_view(), name='tv_list'),
    path('tvdetail/<int:pk>/', views.TvDetailView.as_view(), name='tv_detail'),
    path('tvsearch/', views.SearchView.as_view(), name='tv_search'),
    path('comment_create/<int:pk>/', login_required(views.CommentCreateView.as_view()), name='comment_create'),
    path('login/', views.Login.as_view(), name='login'),
    path('user_create/', views.CustomUserCreationView.as_view(), name='user_create'),
    path('mypage/<int:pk>/', views.MyPage.as_view(), name='mypage'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('logout/', views.Logout.as_view(), name='logout'),
    ]
