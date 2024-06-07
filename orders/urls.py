from . import views 
from django.urls import path

urlpatterns = [
    path('add/<uuid:item_id>/', views.add, name='order'),
    path('<uuid:order_id>/pay/', views.pay, name='pay'),
    path('pay_all/', views.pay_all, name='pay_all'),
]