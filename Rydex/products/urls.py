from django.urls import path
from . import views

urlpatterns=[

  path('products/',views.product_list,name='product_list'),
  path('products/add',views.add_product,name='add_product'),
  path('products/edit/<int:product_id>',views.edit_product,name='edit_product'),
  path('home/product_details/<int:product_id>',views.productDetails,name='product_details'),
  path('products/<int:product_id>/variants',views.variant_list,name='variant_list'),
  path('products/<int:product_id>/variants/add',views.add_variant,name='add_variant'),
  path('products/variants/<int:Variant_id>/edit/', views.edit_variant, name='edit_variant'),
  path('products/<int:product_id>/toggle-status/',views.toggle_product_status,name='toggle_product_status'),
  path('all_products',views.all_products,name='all_products')

]