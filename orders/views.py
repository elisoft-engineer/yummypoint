from django.shortcuts import redirect, get_object_or_404
from menu.models import Menu
from .models import Order, OrderStatus
from django.db import transaction
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def add(request, item_id):
    item = get_object_or_404(Menu, id=item_id)
    if item is not None:
        user = request.user
        amount = item.price
        Order.objects.create(item=item, amount=amount, customer=user)
        messages.success(request, "Order placed successfully")
        return redirect('menu')
    messages.error(request, "Menu Item not found")
    return redirect("menu")

@login_required
def pay(request, order_id):
    user = request.user
    wallet = user.wallet
    order = get_object_or_404(Order, id=order_id)
    total = order.amount
    if total <= wallet.amount:
        with transaction.atomic():
            wallet.amount -= total
            wallet.save()
            order.status = OrderStatus.PAID
            order.save()
        messages.success(request, "Payment made successfully")
    else:
        messages.error(request, "Payment unsuccessful. Please top up your wallet")
    return redirect("account")

@login_required
def pay_all(request):
    user = request.user
    wallet = user.wallet
    orders = user.orders.filter(status=OrderStatus.PENDING)
    total_dict = orders.aggregate(total=Sum('amount'))
    total = total_dict['total'] if total_dict['total'] is not None else 0

    if total <= wallet.amount:
        with transaction.atomic():
            wallet.amount -= total
            wallet.save()
            orders.update(status=OrderStatus.PAID)
        messages.success(request, "Payment made successfully")
    else:
        messages.error(request, "Payment unsuccessful. You either have no pending orders or wallet lacks enough amount")

    return redirect("account")

