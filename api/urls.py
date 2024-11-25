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
]
