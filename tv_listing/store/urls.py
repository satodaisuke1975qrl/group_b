from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'store'

urlpatterns = [
    path('home/', views.Home.as_view(), name='home'),
    path('detail/<int:pk>/', views.GoodsDetail.as_view(), name='detail'),
    path('add_sessioncart/', views.SessionAddToCart.as_view(), name='add_sessioncart'),
    path('sessioncontent/', views.SessionCartContent.as_view(), name='sessioncart_content'),
    path('add_modelcart/', views.ModelAddToCart.as_view(), name='add_modelcart'),
    path('modelcontent/<int:pk>/', views.ModelCartContent.as_view(), name='modelcart_content'), # pk は CartUnitのpk
    path('delete_modelcart/', views.ModelCartDelete.as_view(), name='modelcart_delete'),
    path('delete_sessioncart/', views.SessionCartDelete.as_view(), name='sessioncart_delete'),
    path('purchase/preview/', views.PurchasePreview.as_view(), name='purchase_preview'),
    path('purchase/_process/', views.PurchaseProcess.as_view(), name='_purchase_process'),
    path('purchase/done/', views.PurchaseDone.as_view(), name='purchase_done'),
]

