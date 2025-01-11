from django.urls import path
from . import views

urlpatterns=[
  path('cart',views.cart_view,name='cart_view'),
  path('cart/add/<int:variant_id>/',views.add_to_cart,name='add_to_cart'),
  path('remove_cart_item/<int:item_id>/',views.remove_cart_item,name='remove_cart_item'),
  path('update_cart',views.update_cart,name='update_cart'),
  path('wishlist',views.wishlist_view,name='wishlist'),
  path('add_to_wishlist/<int:variant_id>',views.add_to_wishlist,name='add_to_wishlist'),
  path('remove_from_wishlist/<int:variant_id>',views.remove_from_wishlist,name='remove_from_wishlist'),
  

]