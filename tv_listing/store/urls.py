from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'store'

urlpatterns = [
    path('home/', views.Home.as_view(), name='home'),

    ]
