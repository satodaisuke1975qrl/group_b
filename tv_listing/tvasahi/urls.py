from django.urls import path
from . import views

app_name = 'tvasahi'

urlpatterns = [
    path('home/', views.Home.as_view(), name='home')
    ]
