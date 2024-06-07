from django.db import models
from menu.models import Menu
from accounts.models import User
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
    item = models.ForeignKey(Menu ,on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0.01)])
    date = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    status = EnumField(OrderStatus, default=OrderStatus.PENDING)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date} - {self.item.name}"

