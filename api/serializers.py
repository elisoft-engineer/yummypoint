from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import Customer, Admin
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.serializerfields import PhoneNumberField as DRFPhoneNumberField


"""
All serializers for the api
"""


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims (if needed in the token payload)
        token['email'] = user.email
        token['is_active'] = user.is_active
        token['is_customer'] = user.is_customer
        token['is_admin'] = user.is_admin

        return token

    def validate(self, attrs):
        # Get the default token pair data
        data = super().validate(attrs)

        # Add custom user data to the response
        user = self.user
        user_data = {
            'user_id': user.id,
            'email': user.email,
            'is_customer': user.is_customer,
            'is_admin': user.is_admin,
        }

        # If user is a customer, add customer-specific fields
        if user.is_customer:
            customer = Customer.objects.get(id=user.id)
            user_data.update({
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'phone': str(customer.phone),
                'address': customer.address,
                'wallet': str(customer.wallet),
                'image_url': customer.image.url,
            })

        # If user is a admin, add admin-specific fields
        if user.is_admin:
            admin = Admin.objects.get(id=user.id)
            user_data.update({
                'employee_id': admin.employee_id,
            })

        # Add user data to the token response
        data.update(user_data)

        return data