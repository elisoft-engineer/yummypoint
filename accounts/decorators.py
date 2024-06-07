from functools import wraps
from django.urls import reverse
from .models import Admin, Customer
from django.shortcuts import redirect
from core import settings
from django.contrib import messages

"""
Since there are more than one group of users i.e. customers, and admin, we cannot
rely on the login_required decorator from django.contrib.auth.decorators
That's why we need to define our custom decorators to efficiently detect and 
redirect each type of user without writing boilerplate code.
In every case we first check for the user's authentication status. If the user 
is authenticated, we attach the user object to the kwargs keeping in mind their
respective group. In case they aren't logged in, we deny them the access 
whatsoever. We may opt to redirect them to the customer page for customer signin 
but this might be quite insecure since it might give the user a hint of 
whatever that is going on i.e. the possibility of signing in as a user
of another group.
"""

def customer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session["next"] = request.get_full_path()
            messages.error(request, "You need to login as a customer before proceeding")
            return redirect(reverse(settings.CUSTOMER_LOGIN_URL))
        try:
            customer = Customer.objects.get(email=request.user.email)
        except Customer.DoesNotExist:
            messages.error(request, f"Access Denied")
            return redirect(request.get_full_path())
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
        except admin.DoesNotExist:
            messages.error(request, f"Access Denied")
            return redirect(request.get_full_path())
        return view_func(request, admin=admin, *args, **kwargs)
    return wrapper