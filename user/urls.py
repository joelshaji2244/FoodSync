from django.urls import path
from user import views

urlpatterns = [
    path('signin/', views.CustomerSignInView.as_view(), name="user_signin"),
    path('logout/',views.logoutView, name="user_logout"),
    path('',views.IndexView.as_view(), name="user_index"),
    path('restaurant/<int:pk>/detail/',views.RestaurantDetailView.as_view(),name="user_restaurant_detail"),
    path('restaurant/detail/<int:pk>/addtocart/',views.add_to_cart,name="add_to_cart"),
    path('cart/',views.CartListView.as_view(),name="cart_list"),
    path('cart/<int:pk>/remove',views.cartremove,name="cart_remove"),
]