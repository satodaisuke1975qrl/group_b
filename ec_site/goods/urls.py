from django.urls import path
from goods import views as goods_v

app_name = 'goods'
urlpatterns = [
    path('detail/<int:pk>/', goods_v.GoodsDetail.as_view(), name='detail'),
]
