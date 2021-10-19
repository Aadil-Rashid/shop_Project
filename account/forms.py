from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm)

from .models import Customer, Address


class UserRegisterForm(forms.ModelForm):
    user_name = forms.CharField(label="Enter Username", min_length=4, max_length=50, )
    email = forms.EmailField(label="Enter email", max_length=150, error_messages={'required':'Sorry, you will need an email for registration purpose'})
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    
    # class meta gives us nested name space for configurations and keeps the configurations in one place
    class Meta:
        model = get_user_model()
        fields = ("user_name", "email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("Please use another Email, As this email is already registered")
        return email
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class':'mb-1 mt-1',  'placeholder': 'Enter Username'}
        )
        self.fields['email'].widget.attrs.update(
            {'class':'mb-1 mt-1', 'placeholder': 'Enter Email Id'}
        )
        self.fields['password'].widget.attrs.update(
            {'class':'mb-1 mt-1', 'placeholder': 'Enter Password'}
        )
        self.fields['password2'].widget.attrs.update(
            {'class':'mb-1 mt-1', 'placeholder': 'Repeat Password'}
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'mb-1 mt-1',
            'placeholder': 'Username', 
            'id':'login-user'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class':'mb-1 mt-1',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))


# User edit form
class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account Email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='Account Username (can not be changed)', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-firstname', 'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='First Name',  widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-firstname'}))
    
    middle_name = forms.CharField(
        label='Middle Name',  widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Middlename', 'id': 'form-middlename'}))

    last_name = forms.CharField(
        label='Last Name', widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Lastname', 'id': 'form-lastname'}))

    about = forms.CharField(
        label='About', min_length=5, widget=forms.Textarea(
            attrs={'class': 'form-control mb-3', 'placeholder': 'about', 'id': 'form-about'}))

    mobile_number = forms.CharField(
        label='Mobile Number', max_length=15, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Mobile Number', 'id': 'form-mobilenumber'}))

    class Meta:
        model = Customer
        fields = ('email', 'user_name', 'mobile_number', 'first_name', 'middle_name', 'last_name', 'about')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True



# Password Reset form
class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find your account, Please Register new one')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))


# Address
class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "mobile_number", "state", "district", "address", "LandMark", "town", "postcode",]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["mobile_number"].widget.attrs.update({"class": "form-control mb-2 account-form", "placeholder": "Mobile Number"})
        
        self.fields["state"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "State"}
        )
        self.fields["district"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "District"}
        )
        self.fields["address"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Address"}
        )
        self.fields["LandMark"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Land-Mark"}
        )
        self.fields["town"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Town"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Postal Code"}
        )

