from rest_framework.permissions import BasePermission
from accounts.models import Customer, Admin

class IsCustomer(BasePermission):
    """
    Allows access only to Customers.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_customer


class IsAdmin(BasePermission):
    """
    Allows access only to Admins.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsCustomerOrAdmin(BasePermission):
    """
    Custom permission to allow access to the Customer's details view
    if the user is either the Customer or an Admin.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the Admin (obj is the Admin instance)
        if obj.email == request.user.email:
            return True

        # Check if the user is an admin
        return request.user.is_admin
