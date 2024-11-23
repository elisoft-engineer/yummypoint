from django.urls import path
from . import views

urlpatterns = [
    # customer auth routes
    path('signup/', views.CustomerSignup.as_view(), name='signup'),
    path('signin/', views.CustomerSignin.as_view(), name='signin'),
    path('topup/', views.Topup.as_view(), name='topup'),

    # common auth routes
    path('me/', views.Account.as_view(), name="account"),
    path('signout/', views.Signout.as_view(), name='signout'),
]