from django.urls import path,include
from core import urls
from . import views

urlpatterns=[

  path('',include(urls)),
  path('admin/category_list',views.category_list, name='category_list'),
  path('admin/add_category',views.add_category, name='add_category'),
  path('admin/edit_category/<int:id>',views.edit_category,name='edit_category'),
  path('admin/category_list/list_category/<int:id>',views.list_category,name='list_category'),
  path('admin/category_list/unlist_category/<int:id>',views.unlist_category,name='unlist_category'),
  path('shop_by_category/<int:category_id>',views.shop_by_category,name='shop_by_category'),
  
]