from .models import Menu, Review
from django import forms

class MenuCreateForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["name", "description", "price", "category", "image"]

class MenuUpdateForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["name", "description", "price", "category", "image"]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["content", "rating"]
