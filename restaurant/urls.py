from django.urls import path
from restaurant import views

urlpatterns = [
    path('signup/',views.RestaurantRegistrationView.as_view(),name="restaurant_signup"),
    path('', views.RestaurantSignInView.as_view(), name="restaurant_signin"),
    path('logout/',views.logoutView, name="restaurant_logout"),
    path('index/', views.IndexView.as_view(), name="restaurant_index"),
    path('category/add/',views.CategoryView.as_view(),name="category_add"),
    path('category/<int:pk>/enable/',views.enableCategory,name="category_enable"),
    path('category/<int:pk>/disable/',views.disableCategory,name="category_disable"),
    path('category/<int:pk>/remove/',views.deleteCategory,name="category_delete"),
    path('category/<int:pk>/detail/',views.CategoryListView.as_view(), name="category_list"),
    path('item/add/',views.ItemCreateView.as_view(),name="item_add"),
    path('item/list/',views.ItemListView.as_view(),name="item_list"),
    path('item/<int:pk>/enable/',views.enableItem,name="item_enable"),
    path('item/<int:pk>/disable/',views.disableItem,name="item_disable"),
    path('item/<int:pk>/remove/',views.removeitem,name="item_delete"),
    path('item/<int:pk>/update/',views.ItemUpdateView.as_view(),name="item_update"),
    path('item/<int:pk>/detail/',views.ItemDetailView.as_view(),name="item_detail"),
    path('item/<int:pk>/offer/add/',views.OfferCreateView.as_view(),name="offer_add"),
    path('item/<int:pk>/offer/remove',views.removeoffer,name="offer_delete"),
    path('index/gallery/',views.GalleryUploadView.as_view(),name="gallery_add"),

]