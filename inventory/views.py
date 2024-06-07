from django.shortcuts import render, redirect, get_object_or_404
from .models import Inventory
from .forms import AddForm, UpdateForm
from django.contrib import messages
from accounts.decorators import customer_required, admin_required
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.urls import reverse

class InventoryList(View):
    template_name = "inventory/all.html"
    form_class = AddForm
    admin = None

    @method_decorator(admin_required)
    def dispatch(self, request, admin=None, *args, **kwargs):
        self.admin = admin
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {
            "form" : form,
            "title" : "Inventory",
            "inventory" : Inventory.objects.all(),
        })
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record added successfully")
            return redirect("inventory-list")
        return render(request, self.template_name, {
            "form" : form,
            "title" : "Inventory",
            "inventory" : Inventory.objects.all(),
        })

class InventoryUpdate(View):
    template_name = "inventory/update.html"
    form_class = UpdateForm
    admin = None
    record = None

    @method_decorator(admin_required)
    def dispatch(self, request, admin=None, *args, **kwargs):
        self.admin = admin
        try:
            self.record = Inventory.objects.get(id=kwargs.get("id"))
        except Inventory.DoesNotExist:
            messages.error(request, "Inventory record not found")
            return redirect(reverse("inventory-list"))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.record)
        return render(request, self.template_name, {
            "form" : form,
            "title" : "Inventory | Update",
        })
    
    def post(self, request, *args, **kwargs):
        form = UpdateForm(request.POST, instance=self.record)
        if form.is_valid():
            form.save()
            messages.success(request, "Inventory record updated successfully")
            return redirect(reverse("inventory-list"))
        return render(request, self.template_name, {
            "form" : form,
            "title" : "Inventory | Update",
        })

class InventoryDelete(View):
    admin = None
    record = None

    @method_decorator(admin_required)
    def dispatch(self, request, admin=None, *args, **kwargs):
        self.admin = admin
        try:
            self.record = Inventory.objects.get(id=kwargs.get("id"))
        except Inventory.DoesNotExist:
            messages.error(request, "Inventory record not found")
            return redirect(reverse("inventory-list"))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.record.delete()
        messages.success(request, 'Inventory record deleted successfully')
        return redirect(reverse('inventory-list'))

