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
    amount = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0.01)])
    date = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='orders')
    status = EnumField(OrderStatus, default=OrderStatus.PENDING)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date} - {self.customer.email}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.menu.name} in Order {self.order.id}"



class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="cart")

    def __str__(self):
        return f"Cart for {self.customer}"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    def add_item(self, menu, quantity=1):
        """
        Adds an item to the cart or updates the quantity if the item already exists.
        """
        cart_item, created = CartItem.objects.get_or_create(cart=self, menu=menu)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        return cart_item

    def reduce_item(self, menu):
        """
        Reduce the quantity of an object from the cart.
        """
        try:
            cart_item = CartItem.objects.get(cart=self, menu=menu)
            if cart_item.quantity == 1:
                self.remove_item(menu)
            else:
                cart_item.quantity -= 1
                cart_item.save()
        except CartItem.DoesNotExist:
            raise ValueError("Item not found in cart")


    def remove_item(self, menu):
        """
        Removes an item from the cart.
        """
        try:
            cart_item = self.items.get(menu=menu)
            cart_item.delete()
        except CartItem.DoesNotExist:
            raise ValueError("Item not found in cart")

    def clear_cart(self):
        """
        Removes all items from the cart.
        """
        self.items.all().delete()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.menu.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.menu.name} in Cart {self.cart.customer}"

