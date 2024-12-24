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
    # menu
    path('menu/', views.MenuList.as_view(), name="api-menu-list"),
    path('menu/<uuid:pk>/', views.MenuDetail.as_view(), name="api-menu-detail"),
    # categories
    path('categories/', views.CategoryList.as_view(), name="api-category-list"),
    path('categories/<uuid:pk>/', views.CategoryDetail.as_view(), name="api-category-detail"),
    # reviews
    path('reviews/', views.ReviewList.as_view(), name="api-review-list"),
    path('reviews/<uuid:pk>/', views.ReviewDetail.as_view(), name="api-review-detail"),
    # cart
    path('cart/', views.CartView.as_view(), name="api-cart-view"),
    # orders
    path('orders/', views.OrderList.as_view(), name="api-order-list"),
    path('orders/<uuid:pk>/', views.OrderDetail.as_view(), name="api-order-detail"),
    # notifications
    path('notifications/', views.NotificationList.as_view(), name="api-notification-list"),
    path('notifications/<uuid:pk>/', views.NotificationDetail.as_view(), name="api-notification-detail"),
]
