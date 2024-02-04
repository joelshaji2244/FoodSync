from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.views import View

from restaurant import forms
from myapp import models
from django.views.generic import CreateView,FormView,TemplateView,ListView,DetailView,UpdateView

# Create your views here.

def signinRequired(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"Invalid User")
            return redirect("restaurant_signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


class RestaurantRegistrationView(CreateView):
    template_name = "restaurant/signup.html"
    form_class = forms.RestaurantRegistrationForm
    model = models.Restaurant
    success_url = reverse_lazy("restaurant_signin")

    def form_valid(self, form):
        messages.success(self.request,"Registered Successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Registration Failed")
        return super().form_invalid(form)


class RestaurantSignInView(FormView):
    template_name = 'restaurant/signin.html'
    form_class = forms.SignInForm

    def post(self, request, *args, **kwargs):
        form = forms.SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None and user.user_type == 'restaurant':
                login(request, user)
                return redirect('restaurant_index')
            else:
                messages.error(request,"Invalid login credentials")
                return render(request,self.template_name,{"form":form})

        return render(request, self.template_name,{"form":form})

      
@signinRequired        
def logoutView(request,*args,**kwargs):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect("restaurant_signin")


@method_decorator(signinRequired, name="dispatch")         
class IndexView(ListView):
    template_name = "restaurant/index.html"
    model = models.Category
    context_object_name = "category"

    def get_queryset(self):
        return models.Category.objects.filter(restaurant=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["image"] = models.Gallery.objects.filter(restaurant=self.request.user)
        return context


@method_decorator(signinRequired, name="dispatch") 
class CategoryView(CreateView,ListView):
    template_name = "restaurant/add_category.html"
    form_class = forms.CategoryCreateForm
    model = models.Category
    context_object_name = "category"
    success_url = reverse_lazy("category_add")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.restaurant = self.request.user.restaurant 
        category.save()
        messages.success(self.request,"Category Added Successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Failed to Add Category")
        category_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(form=form, category_list=category_list))
    
    def get_queryset(self):
        return models.Category.objects.filter(restaurant=self.request.user.restaurant)

  
@signinRequired
def enableCategory(request,*args,**kwargs):
    id = kwargs.get("pk")
    models.Category.objects.filter(id=id).update(is_active=True)
    messages.success(request,"Category Enabled Successfully")
    return redirect("category_add")


@signinRequired   
def disableCategory(request,*args,**kwargs):
    id = kwargs.get("pk")
    models.Category.objects.filter(id=id).update(is_active=False)
    messages.success(request,"Category Disabled Successfully")
    return redirect("category_add")


@signinRequired 
def deleteCategory(request,*args,**kwargs):
    id = kwargs.get("pk")
    models.Category.objects.filter(id=id).delete()
    messages.success(request,"Category Deleted Successfully")
    return redirect("category_add")


@method_decorator(signinRequired, name="dispatch")
class CategoryListView(DetailView):
    template_name = "restaurant/category_list.html"
    model = models.Category
    context_object_name = "category"


@method_decorator(signinRequired, name="dispatch")
class ItemCreateView(CreateView):
    template_name = "restaurant/add_item.html"
    model = models.Item
    form_class = forms.ItemCreateForm
    success_url = reverse_lazy("item_list")

    def form_valid(self, form):
        item = form.save(commit=False)
        existing_item = models.Item.objects.filter(name=item.name, restaurant=self.request.user.restaurant).first()
        if existing_item:
            messages.error(self.request, "Item with this name already exists.")
            return self.form_invalid(form)
        item.restaurant = self.request.user.restaurant  # The logged-in restaurant
        item.save()
        messages.success(self.request,"Item Created Succesfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Failed To Add Item")
        return super().form_invalid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@method_decorator(signinRequired, name="dispatch")   
class ItemListView(ListView):
    template_name = "restaurant/item_list.html"
    context_object_name = "item"
    model = models.Item

    def get_queryset(self):
        return models.Item.objects.filter(restaurant=self.request.user.restaurant)
        

@signinRequired
def enableItem(request,*args,**kwargs):
    id = kwargs.get("pk")
    models.Item.objects.filter(id=id).update(is_active = True)
    messages.success(request,"Item Enabled Successfully")
    return redirect("item_list")

@signinRequired
def disableItem(request,*args,**kwargs):
    id = kwargs.get("pk")
    models.Item.objects.filter(id=id).update(is_active = False)
    messages.success(request,"Item Disabled Successfully")
    return redirect("item_list")


@signinRequired   
def removeitem(request,*args,**kwargs):
    id=kwargs.get("pk")
    models.Item.objects.filter(id=id).delete()
    messages.success(request,"Item Removed Successfully")
    return redirect("item_list")


@method_decorator(signinRequired, name="dispatch")
class ItemDetailView(DetailView):
    template_name = "restaurant/item_detail.html"
    model = models.Item
    context_object_name = "item"


@method_decorator(signinRequired, name="dispatch")
class ItemUpdateView(UpdateView):
    template_name = "restaurant/item_update.html"
    form_class = forms.ItemCreateForm
    model = models.Item
    success_url = reverse_lazy("item_list")

    def form_valid(self, form):
        messages.success(self.request,"Item Updated Successfully")
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@method_decorator(signinRequired, name="dispatch")   
class OfferCreateView(CreateView):
    template_name = "restaurant/add_offer.html"
    model = models.Offer
    form_class = forms.OfferAddForm
    # success_url = reverse_lazy("item_detail")

    def form_valid(self, form):
        id = self.kwargs.get("pk")
        item_id = models.Item.objects.get(id=id)
        form.instance.item = item_id
        form.instance.restaurant = self.request.user.restaurant
        messages.success(self.request,"Offer Added Successfully")
        return super().form_valid(form)
     
    def get_success_url(self):
        id=self.kwargs.get("pk")
        item_obj = models.Item.objects.get(id=id)
        return reverse("item_detail",kwargs={"pk":item_obj.id})


@signinRequired   
def removeoffer(request,*args,**kwargs):
    id = kwargs.get("pk")
    offer_obj = models.Offer.objects.get(id=id)
    item_id = offer_obj.item.id
    offer_obj.delete()
    messages.success(request,"Offer Removed Successfully")
    return redirect("item_detail",pk=item_id)





@method_decorator(signinRequired, name="dispatch")   
class GalleryUploadView(CreateView,ListView):
    template_name = "restaurant/upload_image.html"
    model = models.Gallery
    form_class = forms.AddImageForm
    success_url = reverse_lazy("gallery_add")
    context_object_name = "img"

    def form_valid(self, form):
        gallery = form.save(commit=False)
        gallery.restaurant = self.request.user.restaurant 
        gallery.save()
        messages.success(self.request,"Image Added Successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Failed to Add Image")
        gallery_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(form=form, gallery_list=gallery_list))
    
    def get_queryset(self):
        return models.Gallery.objects.filter(restaurant=self.request.user.restaurant)

