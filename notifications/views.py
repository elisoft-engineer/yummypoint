from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from accounts.decorators import customer_required
from django.utils.decorators import method_decorator
from .models import Notification, NotificationStatus
from django.contrib import messages


"""
This file handles all the notification views for the customers.
"""


class NotificationList(View):
    template_name = "notifications/notification-list.html"
    customer = None
    notifications = None

    @method_decorator(customer_required)
    def dispatch(self, request, customer=None, *args, **kwargs):
        self.customer = customer
        self.notifications = self.customer.notifications.all()
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "title": "Notifications",
            "notifications": self.notifications,
            "tally": self.notifications.filter(status=NotificationStatus.UNREAD).count()
        })
    

class NotificationDelete(View):
    customer = None
    notification = None

    @method_decorator(customer_required)
    def dispatch(self, request, customer=None, *args, **kwargs):
        self.customer = customer
        try:
            self.notification = Notification.objects.get(id=kwargs.get('notification_id'))
        except Notification.DoesNotExist:
            messages.error(request, "Notification not found")
            return redirect(reverse("notification-list"))
        if self.notification.user.id != self.customer.id:
            messages.error(request, "Access Denied")
            return redirect(reverse("notification-list"))
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        self.notification.delete()
        messages.success(request, "Notification deleted successfully")
        return redirect(reverse("notification-list"))
    