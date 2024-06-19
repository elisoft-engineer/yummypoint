from .forms import CustomerSignupForm, CustomerSigninForm, CustomerUpdateForm, AdminSignupForm, AdminUpdateForm, AdminSigninForm
from .models import normalize_phone
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.http import QueryDict
from core import settings
from django.utils.decorators import method_decorator
from .decorators import customer_required, admin_required

"""
customer authentication views ... CustomerSignup, CustomerSignin and CustomerUpdate
"""

class CustomerSignup(View):
    template_name = "accounts/signup.html"
    form_class = CustomerSignupForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "title" : "Create an Account",
            "form" : self.form_class()
        })
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            """
            get the password to hash it since by overiding we lack the ability to 
            use the inbuilt user creation password hashing
            """
            password = form.cleaned_data["password"]
            hashed_password = make_password(password)
            """
            we call the form.save() without commiting to enable us set the hashed password
            """
            customer = form.save(commit=False) 
            customer.password = hashed_password
            customer.save()
            customer_group, created = Group.objects.get_or_create(name='Customer')
            customer.groups.add(customer_group)
            """
            Log in the customer after creation of account instead of having them 
            type the credentials
            """
            login(request, customer)
            messages.success(request, "Customer account created successfully")
            return redirect(reverse("menu"))
        return render(request, self.template_name, {"form" : form})

class CustomerSignin(View):
    template_name = "accounts/signin.html"
    form_class = CustomerSigninForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "title" : "Sign In",
            "form" : self.form_class()
        })
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            """
            getting the email or phone from the form. the implementation is in the 
            forms.py -- Customer Signin
            """
            email = form.cleaned_data["email_or_phone"]
            password = form.cleaned_data["password"]
            customer = authenticate(email=email, password=password)
            if customer is not None:
                login(request, customer)
                next_url = request.session.get("next")
                if next_url:
                    del request.session["next"]
                return redirect(next_url or reverse(settings.CUSTOMER_LOGIN_REDIRECT))
            """
            in case a admin is trying to signin through the customer form we 
            return an ordinary error
            """
            messages.success(request, f"signed in as {email}")
            return redirect(reverse("menu"))
        """
        when the form is not valid we just return the customer to the login page 
        with the error detail
        """
        return render(request, self.template_name, {"form" : form})

"""
Admin authentication views ... AdminSignup, AdminSignin and AdminUpdate
"""

class AdminSignup(View):
    template_name = "accounts/admin-signup.html"
    form_class = AdminSignupForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "title" : "Register Admin",
            'form' : self.form_class
        })
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            """
            get the password to hash it since by overiding we lack the ability to use the inbuilt 
            user creation password hashing
            """
            password = form.cleaned_data["password"]
            hashed_password = make_password(password)
            """
            we call the form.save() without commiting to enable us set the hashed 
            password
            """
            admin = form.save(commit=False)
            admin.password = hashed_password
            """
            by default the admin should have the capabilities of a staff so 
            that they can access the admin dashboard
            """
            admin.is_staff = True
            admin.save()
            admin_group, created = Group.objects.get_or_create(name='Admin')
            admin.groups.add(admin_group)
            """
            Log in the admin after creation of account instead of having them 
            type the credentials
            """
            login(request, admin)
            messages.success(request, "Admin account created successfully")
            return redirect(reverse("admin-dashboard"))
        return render(request, self.template_name, {"form" : form})

class AdminSignin(View):
    template_name = "accounts/admin-signin.html"
    form_class = AdminSigninForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form" : self.form_class()})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            admin = authenticate(email=email, password=password)
            if admin is not None:
                login(request, admin)
                next_url = request.session.get("next")
                if next_url:
                    del request.session["next"]
                return redirect(next_url or reverse(settings.ADMIN_LOGIN_REDIRECT))
            messages.error(request, "Error signing you in")
        return render(request, self.template_name, {"form" : form})
    
"""
The following are supposed to be the common views among both user groups ... example, Signout
"""

class Signout(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.info("No user logged in")
            return redirect(reverse('menu'))
        email = user.email
        logout(request)
        messages.info(request, f"{email} logged out")
        return redirect(reverse('index'))


class Account(View):
    template_name = "accounts/account.html"
    user = None
    form_class = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You are not logged in")
            return redirect(reverse("menu"))
        if request.user.is_admin:
            self.form_class = AdminUpdateForm
        else:
            self.form_class = CustomerUpdateForm
        return super().dispatch(request, *args, **kwargs)
        

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "title" : "Update Account",
            "form" : self.form_class(instance=self.user),
        })
    
    def post(self, request, *args, **kwargs):
        if self.user.is_admin:
            form = self.form_class(request.POST, instance=self.admin)
            if form.is_valid():
                form.save()
                messages.success(request, "Account updated successfully")
                return redirect(reverse("account"))
            return render(request, self.template_name, {
                "title" : "Update Account",
                "form" : form
            })
        else:
            """
            Normalizing the phone is crucial for the customers to avoid inconsistencies. 
            This leads to the need for changing the form data before it goes for 
            validation.
            """
            mutable_data = request.POST.copy()
            phone = mutable_data["phone"]
            mutable_data["phone"] = normalize_phone(phone)
            """
            change the data back to a query dict for it to be pushed to a form as the 
            data
            """
            modified_query_dict = QueryDict(mutable_data.urlencode(), mutable=True)
            # initialize the form with the changed data
            form = self.form_class(data=modified_query_dict, instance=self.customer)
            if form.is_valid():
                form.save()
                messages.success(request, "Account updated successfully")
                return redirect(reverse("account"))
            return render(request, self.template_name, {
                "form" : form,
                "title" : "Update Account",
            })
        
"""
The following view handles the top up of the users wallet.
"""
class Topup(View):
    customer = None

    @method_decorator(customer_required)
    def dispatch(self, request, customer=None, *args, **kwargs):
        self.customer = customer
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        self.customer.wallet += 500
        self.customer.save()
        messages.success(request, "Topup of 500 successfully")
        return redirect(reverse("account"))