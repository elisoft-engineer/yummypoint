from functools import wraps
from django.urls import reverse
from .models import Admin, Customer
from django.shortcuts import redirect
from core import settings
from django.contrib import messages

def customer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session["next"] = request.get_full_path()
            print(request.session["next"])
            messages.error(request, "You need to login as a customer before proceeding")
            return redirect(reverse(settings.CUSTOMER_LOGIN_URL))
        try:
            customer = Customer.objects.get(email=request.user.email)
        except Customer.DoesNotExist:
            messages.error(request, f"Access Denied")
            return redirect(reverse("index"))
        return view_func(request, customer=customer, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session["next"] = request.get_full_path()
            messages.error(request, "You need to login as a admin before proceeding")
            return redirect(reverse(settings.ADMIN_LOGIN_URL))
        try:
            admin = Admin.objects.get(email=request.user.email)
        except Admin.DoesNotExist:
            messages.error(request, f"Access Denied")
            return redirect(reverse("index"))
        return view_func(request, admin=admin, *args, **kwargs)
    return wrapper