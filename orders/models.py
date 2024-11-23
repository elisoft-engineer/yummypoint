from django.db import models
from menu.models import Menu
from accounts.models import Customer
from django.utils import timezone
from django.core.validators import MinValueValidator
import uuid
from enumfields import EnumField
from enum import Enum

class OrderStatus(Enum):
    PENDING = 'Pending'
    PAID = 'Paid'
    CANCELLED = 'Cancelled'
    

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    items = models.ManyToManyField(Menu, related_name="orders")
    amount = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0.01)])
    date = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='orders')
    status = EnumField(OrderStatus, default=OrderStatus.PENDING)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date} - {self.item.name}"


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="cart")

    def __str__(self):
        return f"Cart for {self.customer}"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.menu.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.menu.name} in Cart {self.cart.customer}"

