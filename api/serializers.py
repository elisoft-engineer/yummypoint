from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import Customer, Admin
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.serializerfields import PhoneNumberField as DRFPhoneNumberField
from decimal import Decimal
from django.contrib.auth.password_validation import MinimumLengthValidator, NumericPasswordValidator
from django.core.exceptions import ValidationError
from feedback.models import ContactMessage, MessageStatus
from inventory.models import Inventory, Supplier


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
                'image': customer.image.url,
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

    
class PhoneNumberSerializerField(DRFPhoneNumberField):
    def to_representation(self, value):
        if isinstance(value, PhoneNumber):
            return str(value)
        return super().to_representation(value)

    def to_internal_value(self, data):
        return super().to_internal_value(data)


class CustomerSerializer(serializers.ModelSerializer):
    phone = PhoneNumberSerializerField()
    wallet = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.00'))
    class Meta:
        model = Customer
        fields = ['id', 'email', 'phone', 'first_name', 'last_name', 'address', 'wallet', 'image', 'is_active', 'date_joined']


class CustomerCreateSerializer(serializers.ModelSerializer):
    phone = PhoneNumberSerializerField()
    image = serializers.ImageField(required=False)

    class Meta:
        model = Customer
        fields = ['email', 'phone', 'first_name', 'last_name', 'address', 'image', 'password']

    def validate(self, attrs):
        if Customer.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'email': 'A customer with this email already exists.'})

        if Customer.objects.filter(phone=attrs['phone']).exists():
            raise serializers.ValidationError({'phone': 'A customer with this phone already exists.'})

        return attrs

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)



class CustomerUpdateSerializer(serializers.ModelSerializer):
    phone = PhoneNumberSerializerField()
    image = serializers.ImageField(required=False)

    class Meta:
        model = Customer
        fields = ['email', 'phone', 'first_name', 'last_name', 'address', 'image']

    def validate_email(self, value):
        """
        Ensure the email is unique (excluding the current instance).
        """
        if Customer.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("A customer with this email already exists.")
        return value

    def validate_phone(self, value):
        """
        Ensure the phone number is unique (excluding the current instance).
        """
        if Customer.objects.filter(phone=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("A customer with this phone number already exists.")
        return value



"""
Admin Serializers
"""


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'email', 'employee_id', 'is_active', 'date_joined']


class AdminCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['email', 'employee_id', 'password']

    def validate_email(self, value):
        """
        Ensure the email is unique.
        """
        if Admin.objects.filter(email=value).exists():
            raise serializers.ValidationError("An admin with this email already exists.")
        return value

    def validate_employee_id(self, value):
        """
        Ensure the employee_id is unique.
        """
        if Admin.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError("An admin with this employee ID already exists.")
        return value

    def validate_password(self, value):
        """
        Validate password complexity.
        """
        validators = [MinimumLengthValidator(), NumericPasswordValidator()]
        for validator in validators:
            try:
                validator.validate(password=value, user=None)
            except ValidationError as e:
                raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        """
        Use make_password to hash the password.
        """
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)



class AdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['email']

    def validate_email(self, value):
        """
        Ensure the email is unique (excluding the current instance).
        """
        if Admin.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("An admin with this email already exists.")
        return value



class EnumField(serializers.Field):
    def __init__(self, enum_class, *args, **kwargs):
        self.enum_class = enum_class
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        if isinstance(value, self.enum_class):
            return value.value
        return str(value)

    def to_internal_value(self, data):
        try:
            return self.enum_class(data)
        except ValueError:
            raise serializers.ValidationError(f"Invalid value for enum {self.enum_class.__name__}: {data}")
        
    def get_schema(self):
        return {
            "type": "string",
            "enum": [e.value for e in self.enum_class],
        }


class MessageSerializer(serializers.ModelSerializer):
    status = EnumField(enum_class=MessageStatus)
    class Meta:
        model = ContactMessage
        fields = ["id", "name", "email", "message", "status", "sent_at"]


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]


class InventorySerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    class Meta:
        model = Inventory
        fields = ["id", "name", "quantity", "price", "date", "supplier"]

class InventoryCreateSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    class Meta:
        model = Inventory
        fields = ["name", "quantity", "price", "supplier"]



class InventoryUpdateSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    class Meta:
        model = Inventory
        fields = ["name", "quantity", "price", "supplier"]



class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name", "location"]


class SupplierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["name", "location"]


class SupplierUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["name", "location"]
