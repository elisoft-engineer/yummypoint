from . import views 
from django.urls import path

urlpatterns = [
    path('add/<uuid:item_id>/', views.PlaceOrder.as_view(), name='order'),
    path('<uuid:order_id>/pay/', views.Pay.as_view(), name='pay'),
    path('pay_all/', views.PayAll.as_view(), name='pay_all'),
]