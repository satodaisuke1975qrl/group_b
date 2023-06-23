from django.urls import path
from . import views

app_name = 'tvasahi'

urlpatterns = [
    path('home/', views.Home.as_view(), name='home'),
    path('tvlist/<int:pk>/', views.TvListView.as_view(), name='tv_list'),
    path('tvdetail/<int:pk>/', views.TvDetailView.as_view(), name='tv_detail'),
    path('tvsearch/', views.SearchView.as_view(), name='tv_search')
    ]
