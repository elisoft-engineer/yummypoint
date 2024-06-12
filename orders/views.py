from django.shortcuts import redirect
from menu.models import Menu
from .models import Order, OrderStatus
from django.db import transaction
from django.db.models import Sum
from django.contrib import messages
from django.views.generic import View
from accounts.decorators import customer_required, admin_required
from django.urls import reverse
from django.utils.decorators import method_decorator

class PlaceOrder(View):
    customer = None
    item = None

    @method_decorator(customer_required)
    def dispatch(self, request , customer=None, *args, **kwargs):
        self.customer = customer
        try:
            self.item = Menu.objects.get(kwargs.get(id='item_id'))
        except Menu.DoesNotExist:
            messages.error(request, "Menu Item not found")
            return redirect(reverse("menu"))
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        amount = self.item.price
        Order.objects.create(item=self.item, amount=amount, customer=self.customer)
        messages.success(request, "Order placed successfully")
        return redirect(reverse("menu"))

class Pay(View):
    customer = None
    order = None

    @method_decorator(customer_required)
    def dispatch(self, request , customer=None, *args, **kwargs):
        self.customer = customer
        try:
            self.order = Order.objects.get(kwargs.get(id='order_id'))
        except Order.DoesNotExist:
            messages.error(request, "Error occured")
            return redirect(reverse("account"))
        if self.order.customer != self.customer:
            messages.error(request, "Access denied")
            return redirect(reverse("account"))
        if self.order.status == OrderStatus.PAID:
            messages.info(request, "The order is already paid for")
            return redirect(reverse("account"))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.order.amount > self.customer.wallet:
            messages.error(request, "Payment unsuccessful. Please top up your wallet")
        else:
            with transaction.atomic():
                self.customer.wallet -= self.order.amount
                self.customer.save()
                self.order.status = OrderStatus.PAID
                self.order.save()
            messages.success(request, "Payment made successfully")
        return redirect(reverse("account"))
    

class PayAll(View):
    customer = None

    @method_decorator(customer_required)
    def dispatch(self, request, customer=None, *args, **kwargs):
        self.customer = customer
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        orders = self.customer.orders.filter(status=OrderStatus.PENDING)
        total_dict = orders.aggregate(total=Sum('amount'))
        total = total_dict['total'] if total_dict['total'] is not None else 0

        if self.order.amount > self.customer.wallet:
            messages.error(request, "Payment unsuccessful. You either have no pending orders or wallet lacks enough amount")
        else:
            with transaction.atomic():
                self.customer.wallet -= total
                self.customer.save()
                orders.update(status=OrderStatus.PAID)
            messages.success(request, "Payment made successfully")
        return redirect(reverse("account"))
