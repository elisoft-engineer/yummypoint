from django import forms
from .models import Inventory

class AddForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ["name", "quantity", "price", "supplier"]

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ["name", "quantity", "price", "supplier"]