from django import forms
from django.contrib.auth.forms import UserCreationForm
from myapp import models


class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = models.Customer
        fields = ['username', 'password1', 'password2', 'name', 'email', 'phone', 'street_address', 'city', 'pincode']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'customer'
        
        if commit:
            user.save()

        customer = super(CustomerRegistrationForm, self).save(commit=False)
        customer.user = user
        customer.save()

        return user
    

class SignInForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
