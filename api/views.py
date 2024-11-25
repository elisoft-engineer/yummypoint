from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import Group
from rest_framework_simplejwt.views import TokenObtainPairView
from notifications.models import Notification, NotificationStatus
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied, ValidationError
from .serializers import CustomTokenObtainPairSerializer, CustomerSerializer, CustomerCreateSerializer, \
    AdminSerializer, AdminUpdateSerializer, AdminCreateSerializer, CustomerUpdateSerializer
from .permissions import IsAdmin, IsCustomer, IsCustomerOrAdmin
from accounts.models import Customer, Admin
from notifications.utils import create_notification
from django.urls import reverse


"""
This file handles all the views that handle api routes.
"""


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


"""
This file handles all the views that handle api routes.
"""


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomerList(APIView):
    """
    Endpoint to handle both fetching all customers and creating a new customer.
    Only admins can fetch all customers; any user can create a customer.
    """

    allowed_methods = ['GET', 'POST']
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomerCreateSerializer
        return CustomerSerializer


    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]  # No restriction on POST method
        elif self.request.method == 'GET':
            return [IsAdmin()]  # Restrict GET method to admins only
        return [IsAuthenticated]

    def get(self, request):
        """
        Handle GET request to fetch all customers.
        """
        active = request.query_params.get('active', None)
        if active is not None:
            active = active.lower() in ['true', '1', 'yes']
            customers = Customer.objects.filter(is_active=active)
        else:
            customers = Customer.objects.all()

        serializer = self.get_serializer_class()(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handle POST request to create a new customer.
        """
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            customer_group, _ = Group.objects.get_or_create(name="Customer")
            customer.group = customer_group
            customer.save()
            create_notification(customer, "Welcome to Yummy Point")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AdminList(APIView):
    """
    Endpoint to handle both fetching all admins and creating a new admin.
    Only accessible to admins.
    """

    allowed_methods = ['GET', 'POST']
    permission_classes = [IsAdmin]  # Apply IsAdmin permission for all methods

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdminCreateSerializer
        return AdminSerializer

    def get(self, request):
        """
        Handle GET request to fetch all admins.
        """
        active = request.query_params.get('active', None)
        if active is not None:
            active = active.lower() in ['true', '1', 'yes']
            admins = Admin.objects.filter(is_active=active)
        else:
            admins = Admin.objects.all()

        serializer = self.get_serializer_class()(admins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handle POST request to create a new admin.
        """
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            admin = serializer.save()
            admin_group, _ = Group.objects.get_or_create(name="Admin")
            admin.group = admin_group
            admin.save()
            create_notification(admin, "Welcome to the Yummy Point Team")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(APIView):
    """
    Retrieve, update, or delete a customer instance.
    """

    allowed_methods = ['GET', 'PUT', 'DELETE']
    permission_classes =  [IsAuthenticated, IsCustomerOrAdmin]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CustomerUpdateSerializer
        return CustomerSerializer

    def get_object(self, pk):
        return get_object_or_404(Customer, pk=pk)

    def get(self, request, pk):
        """
        Retrieve customer details.
        """
        customer = self.get_object(pk)
        serializer = self.get_serializer_class()(customer)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a customer.
        """
        customer = self.get_object(pk)
        serializer = self.get_serializer_class()(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a customer.
        """
        customer = self.get_object(pk)
        customer.delete()
        return Response({"detail": "Customer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class AdminDetail(APIView):
    """
    Retrieve, update, or delete a admin instance.
    """

    allowed_methods = ['GET', 'PUT', 'DELETE']
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return AdminUpdateSerializer
        return AdminSerializer

    def get_object(self, pk):
        return get_object_or_404(Admin, pk=pk)

    def get(self, request):
        """
        Retrieve admin details.
        """
        admin = self.get_object(self.request.user.id)
        serializer = self.get_serializer_class()(admin)
        return Response(serializer.data)

    def put(self, request):
        """
        Update an admin.
        """
        admin = self.get_object(self.request.user.id)
        serializer = self.get_serializer_class()(admin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Delete an admin.
        """
        admin = self.get_object(self.request.user.id)
        admin.delete()
        return Response({"detail": "Admin deleted successfully"}, status=status.HTTP_204_NO_CONTENT)