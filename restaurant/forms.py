from django import forms
from django.contrib.auth.forms import UserCreationForm

from myapp import models


class RestaurantRegistrationForm(UserCreationForm):
    class Meta:
        model = models.Restaurant
        fields = ['username', 'password1', 'password2', 'name', 'licence_number', 'image', 'phone', 
                  'street_address', 'city', 'email', 'pincode', 'date_joined']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'restaurant'
        
        if commit:
            user.save()

        restaurant = super(RestaurantRegistrationForm, self).save(commit=False)
        restaurant.user = user
        restaurant.save()

        return user

   
class SignInForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = models.Category
        exclude = ("restaurant", )

class ItemCreateForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        super(ItemCreateForm,self).__init__(*args,**kwargs)
        self.fields["category"].queryset = models.Category.objects.filter(is_active=True,restaurant = self.request.user)
        

    class Meta:
        model = models.Item
        exclude = ("restaurant", )
        widgets = {
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "category":forms.Select(attrs={"class":"form-control"}),
            "image":forms.FileInput(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-control w-25"}),
            "is_active":forms.CheckboxInput(attrs={"class":"form-check-input"})
        }
        labels ={
            "is_active":"Enable/Disable"
        }


class OfferAddForm(forms.ModelForm):
    class Meta:
        model = models.Offer
        exclude = ("restaurant","item")
        widgets={
            "start_date":forms.TextInput(attrs={"type":"date","class":"form-control"}),
            "end_date":forms.TextInput(attrs={"type":"date","class":"form-control"})
        }


class AddImageForm(forms.ModelForm):
    class Meta:
        model = models.Gallery
        exclude = ("restaurant",)