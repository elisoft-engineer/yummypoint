from . import views
from django.urls import path
from accounts.views import AdminSignin

urlpatterns = [
    path("", views.Dashboard.as_view(), name="dashboard"),
    path("signin/", AdminSignin.as_view(), name="admin-signin"),
]
