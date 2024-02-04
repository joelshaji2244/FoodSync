from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import AbstractUser
import math

from django.db.models.signals import post_save

# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')

class Customer(CustomUser):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pincode = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Restaurant(CustomUser):
    name = models.CharField(max_length=255)
    licence_number = models.CharField(max_length=255,unique=True)
    image = models.ImageField(upload_to='restaurant_images/', null=True, blank=True)
    phone = models.CharField(max_length=15)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pincode = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images",null=True)
    is_active = models.BooleanField(default=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)
    image = models.ImageField(upload_to="images")
    price = models.PositiveIntegerField()
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return self.name
    
    @property
    def offer(self):
        return self.offer_set.all()
    
  
class Offer(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    price=models.PositiveIntegerField()
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)

    @property
    def offer_percentage(self):
        price = ((self.item.price-self.price)/self.item.price)*100
        offer_price = str(price)
        p = offer_price[0:4]
        return p
    

class Gallery(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="gallery",null=True)
    is_active = models.BooleanField(default=True)

    
class Cart(models.Model):
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE,related_name="cart")
    options=(
        ("in-cart","in-cart"),
        ("order-placed","order-placed"),
        ("cancelled","cancelled")
    )
    status = models.CharField(max_length=200,choices=options,default="in-cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @property
    def cart_items(self):
        qs=self.cartitem.all()
        return qs
    
    @property
    def cart_item_count(self):
        return self.cartitem.all().count()
    
    @property
    def sub_total(self):
        cart_items=self.cart_items
        if cart_items:
            total=sum([ item.total for item in cart_items ])
            return total
        else:
            return 0


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cartitem") 
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @property
    def total(self):
        if self.item.offer_set.exists():
            # If there is an active offer, use the offer price for calculation
            offer_price = self.item.offer_set.first().price
            return self.quantity * offer_price
        else:
            # If there is no offer, use the regular price for calculation
            return self.quantity * self.item.price


class Order(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    options=(
      
        ("order-placed","order-placed"),
        ("cancelled","cancelled"),
        ("dispatched","dispatched"),
        ("in-transit","in-transit"),
        ("delivered","delivered")
    )
    status=models.CharField(max_length=200,choices=options,default="order-placed")
    ordered_date=models.DateTimeField(auto_now_add=True)
    expected_date=models.DateField(null=True)
    address=models.CharField(max_length=200)

class Review(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,null=True,on_delete=models.SET_NULL)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment = models.CharField(max_length=300)

def create_cart(sender,created,instance,**kwargs):
    if created:
        Cart.objects.create(customer=instance)

post_save.connect(create_cart,sender=Customer)