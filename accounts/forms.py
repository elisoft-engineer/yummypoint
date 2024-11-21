from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import MinimumLengthValidator, NumericPasswordValidator, UserAttributeSimilarityValidator, CommonPasswordValidator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Customer, Admin
from phonenumber_field.phonenumber import PhoneNumber
import phonenumbers

"""
This file contains all the forms used in this app. They handle creation, signin as 
well as update data for all the users in the system i.e. customers and admins.
The necessary cleaning and validation of form data is done via the implemented or 
the inherited clean method.
"""

class CustomerSignupForm(forms.ModelForm):
    # add a confirm password field
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Customer
        fields = ['email', 'phone', 'password', 'confirm_password']
        widgets = {
            'password' : forms.PasswordInput(),
        }
    def clean(self):
        cleaned_data = super().clean()

        # We have to make sure that a user with that email or phone doesn't exist

        if Customer.objects.filter(email=cleaned_data["email"]).exists():
            self.add_error("email", ValidationError("customer with that email already exists"))

        phone = cleaned_data.get("phone")
        if phone:
            try:
                phone_number = PhoneNumber.from_string(phone.as_e164, None)
                normalized_phone = phone_number.as_e164
                cleaned_data["phone"] = normalized_phone
            except phonenumbers.phonenumberutil.NumberParseException:
                self.add_error("phone", ValidationError("Invalid phone number"))
            else:
                if Customer.objects.filter(phone=normalized_phone).exists():
                    self.add_error("phone", ValidationError("customer with that phone already exists"))

        # the passwords must match, be alphanumeric

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error("confirm_password", ValidationError("Passwords do not match")) 
        else:
            user = self.instance
            validators = [MinimumLengthValidator(), NumericPasswordValidator()]
            """
            UserAttributeSimilarityValidator and CommonPasswordValidatorcan also 
            be added. I choose not to as this will make it tougher for the customers 
            to create the password
            """
            for validator in validators:
                try:
                    validator.validate(password=password, user=user)
                except ValidationError as e:
                    self.add_error("password", e)

        return cleaned_data

class CustomerSigninForm(forms.Form):
    # the customer will enter a phone number or an email
    email_or_phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'email or phone'}))
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']

        cred = None
        try:
            # we convert the credential to str so that we can check if its an email
            cred = str(cleaned_data['email_or_phone'])
        except ValueError:
            self.add_error(None, ValidationError("Invalid Credentials"))

        try:
            validate_email(cred)
            cleaned_data["email_or_phone"] = cred
        except ValidationError:
            try:
                """
                We return the cleaned data having an email even when a user types a phone. This is due to the nature 
                of the authenticate function. It authenticates the users across the User model and in our case the 
                phone field is only in the customer model.
                """
                customer = Customer.objects.get(phone=cred)
                cleaned_data["email_or_phone"] = customer.email
            except Customer.DoesNotExist:
                self.add_error(None, ValidationError("Invalid Credentials"))
                return cleaned_data

        customer = authenticate(email=cleaned_data["email_or_phone"], password=password)
        if customer is None:
            self.add_error(None, ValidationError("Invalid Credentials"))
        return cleaned_data

class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'phone', 'first_name', 'last_name', 'image', 'address']


"""
admin forms are defined below.
"""
    
class AdminSignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Admin
        fields = ['email', 'employee_id', 'password', 'confirm_password']
        widgets = {
            'password' : forms.PasswordInput(),
        }
    def clean(self):
        cleaned_data = super().clean()

        """
        A admin account must have a unique email and if a web address, it also 
        has to be unique.
        """

        if Admin.objects.filter(email=cleaned_data["email"]).exists():
            self.add_error("email", ValidationError("admin with that email already exists"))

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error("confirm_password", ValidationError("Passwords do not match")) 
        else:
            user = self.instance

            # for the admin account, the password strength has to be enhanced
            validators = [UserAttributeSimilarityValidator(user_attributes=("email", "website")), CommonPasswordValidator(), NumericPasswordValidator(), MinimumLengthValidator()]
            for validator in validators:
                try:
                    validator.validate(password=password, user=user)
                except ValidationError as e:
                    self.add_error("password", e)

        return cleaned_data

class AdminSigninForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data["email"]
        password = cleaned_data["password"]

        try:
            admin = Admin.objects.get(email=email)
        except Admin.DoesNotExist:
            raise ValidationError("Email or Password incorrect")
        
        if admin:
            admin = authenticate(email=email, password=password)
            if admin is None:
                raise forms.ValidationError("Email or Password incorrect")
        
        return cleaned_data

    
class AdminUpdateForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['email']
