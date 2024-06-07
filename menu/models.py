from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from django.utils import timezone
from accounts.models import User

class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0.01)])
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name="items")
    image = models.ImageField(upload_to='menu/original', default="menu/original/default.png")
    thumbnail = models.ImageField(upload_to='menu/thumbnails', default='menu/thumbnails/default.png')

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        ordering = ["id"]

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    item = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.TextField()
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.reviewer.username} - {self.date.year}/{self.date.month}/{self.date.day}"
    
    class Meta:
        ordering = ['-date']

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

