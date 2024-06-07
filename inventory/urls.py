from . import views
from django.urls import path

urlpatterns = [
    path('', views.InventoryList.as_view(), name='inventory-list'),
    path('<uuid:id>/update/', views.InventoryUpdate.as_view(), name="inventory-update"),
    path('<uuid:id>/delete/', views.InventoryDelete.as_view(), name="inventory-delete"),
]