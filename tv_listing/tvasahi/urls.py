from django.urls import path
from . import views

app_name = 'tvasahi'

urlpatterns = [
    path('home/', views.Home.as_view(), name='home'),
    path('tvlist/', views.TvListView.as_view(), name='tv_list')
    ]
