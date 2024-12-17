from django.urls import path
from . import views

urlpatterns=[

  path('admin_dashboard/products/',views.product_list,name='product_list'),
  path('admin_dashboard/products/add',views.add_product,name='add_product'),
  path('admin_dashboard/products/edit/<int:product_id>',views.edit_product,name='edit_product'),
  path('home/product_details/<int:product_id>',views.productDetails,name='productDetails')
]