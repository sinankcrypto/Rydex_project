from django.urls import path
from . import views

urlpatterns=[
  path('offers_list/',views.offer_list,name='offers_list'),
  path('add_product_offer/',views.add_product_offer,name='add_product_offer'),
  path('edit_product_offer/<int:offer_id>/',views.edit_product_offer,name='edit_product_offer'),
  path('delete_product_offer/<int:offer_id>/',views.delete_product_offer,name='delete_product_offer'),
  path('add_category_offer/',views.add_category_offer,name='add_category_offer'),
  path('edit_category_offer/<int:offer_id>/',views.edit_category_offer,name='edit_category_offer'),
  path('delete_category_offer/<int:offer_id>/',views.delete_category_offer,name='delete_category_offer')
  
]