from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Customer
from orders.models import Cart

"""
This file contains the signals needed to ensure the existence of user groups when 
there's a db migration.
"""

def create_groups():
    roles = {
        'customer': 'Customer',
        'admin': 'Admin',
    }
    for role_name, group_name in roles.items():
        group, created = Group.objects.get_or_create(name=group_name)

@receiver(post_migrate)
def create_groups_handler(sender, **kwargs):
    if sender.name == 'accounts':
        create_groups()

@receiver(post_save, sender=Customer)
def create_cart_for_user(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(customer=instance)
