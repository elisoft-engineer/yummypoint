from django.urls import path
from . import views

urlpatterns = [
    # customer auth routes
    path('signup/', views.CustomerSignup.as_view(), name='signup'),
    path('signin/', views.CustomerSignin.as_view(), name='signin'),
    path('topup/', views.Topup.as_view(), name='topup'),

    # admin auth routes
    path('signup/admin/', views.AdminSignup.as_view(), name='admin-signup'),
    path('signin/admin/', views.AdminSignin.as_view(), name='admin-signin'),

    # common auth routes
    path('me/', views.Account.as_view(), name="account"),
    path('signout/', views.Signout.as_view(), name='signout'),
]
