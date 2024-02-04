from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.views import View

from user import forms
from myapp import models
from django.views.generic import CreateView,FormView,TemplateView,ListView,DetailView

# Create your views here.

def signinRequired(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"Signin Required")
            return redirect("user_signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

  
class IndexView(CreateView,ListView):
    template_name = "user/index.html"
    form_class = forms.CustomerRegistrationForm
    model = models.Customer
    success_url = reverse_lazy("user_signin")

    def form_valid(self, form):
        messages.success(self.request,"Registered Successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Registration Failed")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context ={
           'restaurant': models.Restaurant.objects.all(),
           'categories': models.Category.objects.all(),
           'items': models.Item.objects.all(),
           'offers':models.Offer.objects.all(),
        } 
        return context

class CustomerSignInView(FormView):
    template_name = 'user/signin.html'
    form_class = forms.SignInForm

    def post(self, request, *args, **kwargs):
        form = forms.SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None and user.user_type == 'customer':
                login(request, user)
                return redirect('user_index')
            else:
                messages.error(request,"Invalid login credentials")
                return render(request,self.template_name,{"form":form})

        return render(request, self.template_name,{"form":form})

@signinRequired
def logoutView(request,*args,**kwargs):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect("user_index")

class RestaurantDetailView(DetailView):
    template_name = "user/restaurant_detail.html"
    model = models.Restaurant
    context_object_name = "rest"


@signinRequired
def add_to_cart(request,*args,**kwargs):
    id = kwargs.get("pk")
    item_object = models.Item.objects.get(id=id)
    cart_object = request.user.customer.cart

    cart_item, created = models.CartItem.objects.get_or_create(cart=cart_object, item=item_object)
    print(created)
    # If the item is already in the cart, increase the quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    messages.success(request,"Item Added to Cart")
    
    return redirect("cart_list")

@method_decorator(signinRequired, name="dispatch") 
class CartListView(ListView):
    template_name = "user/cart_list.html"
    model = models.CartItem
    context_object_name = "cartitem"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = models.Cart.objects.filter(customer=self.request.user)
        return context
    
    def get_queryset(self):
        return models.CartItem.objects.filter(cart__customer=self.request.user)


@signinRequired
def cartremove(request,*args,**kwargs):
    id = kwargs.get("pk")
    models.CartItem.objects.filter(id=id).delete()
    messages.success(request,"Item Removed")
    return redirect("cart_list")
