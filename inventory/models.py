from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
import uuid

class Inventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10, validators = [MinValueValidator(0.01)])
    date = models.DateTimeField(default=timezone.now)
    supplier = models.ForeignKey("Supplier", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        ordering = ["-date"]

class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"
