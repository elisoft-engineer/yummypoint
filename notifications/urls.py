from django.urls import path
from . import views


urlpatterns = [
    path('', views.NotificationList.as_view(), name="notification-list"),
    path('<uuid:notification_id>/delete/', views.NotificationDelete.as_view(), name="notification-delete"),
]