from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


urlpatterns = [
    # authentication
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # accounts
    path('customers/', views.CustomerList.as_view(), name="api-customer-list"),
    path('customers/<uuid:pk>/', views.CustomerDetail.as_view(), name="api-customer-detail"),
    path('admins/', views.AdminList.as_view(), name="api-admin-list"),
    path('admins/me/', views.AdminDetail.as_view(), name="api-admin-detail"),
    # messages
    path('messages/', views.MessageList.as_view(), name="api-message-list"),
    path('messages/<uuid:pk>/', views.MessageDetail.as_view(), name="api-message-detail"),
    # inventory
    path('inventory/', views.InventoryList.as_view(), name="api-inventory-list"),
    path('inventory/<uuid:pk>/', views.InventoryDetail.as_view(), name="api-inventory-detail"),
    # suppliers
    path('suppliers/', views.SupplierList.as_view(), name="api-supplier-list"),
    path('suppliers/<uuid:pk>/', views.SupplierDetail.as_view(), name="api-supplier-detail"),
]
