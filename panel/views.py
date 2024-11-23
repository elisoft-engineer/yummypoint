from django.shortcuts import render
from django.views.generic import View
from accounts.decorators import admin_required
from django.utils.decorators import method_decorator


class Dashboard(View):
    template_name = "panel/dashboard.html"
    admin = None

    @method_decorator(admin_required)
    def dispatch(self, request, admin=None, *args, **kwargs):
        self.admin = admin
        return super().dispatch(request, args, kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "title" : "Admin Dashboard",
            "admin" : self.admin,
        })
