from django.urls import path
from . import views

urlpatterns=[
  path('add_coupon/',views.add_coupon,name='add_coupon'),
  path('edit_coupon/<int:coupon_id>',views.edit_coupon,name='edit_coupon'),
  path('delete_coupon/<int:coupon_id>',views.coupon_delete,name='delete_coupon'),
  path('coupon_list/',views.coupon_list,name='coupon_list'),
  path('apply_coupon/',views.apply_coupon,name='apply_coupon')
]