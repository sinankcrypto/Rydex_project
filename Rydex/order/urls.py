from django.urls import path
from . import views

urlpatterns=[
  path('add_address',views.add_address,name='add_address'),
  path('edit_address/<int:address_id>',views.edit_address,name='edit_address'),
  path('delete_address/<int:address_id>',views.delete_address,name='delete_address'),
  path('payment',views.payment,name='payment'),
  path('succes/<int:order_id>',views.success,name='success'),
  path('order_list',views.order_list,name='order_list'),
  path('order_list/update/<int:order_id>',views.update_order_status,name='update_order_status'),
  path('user_orders',views.user_orders,name='user_orders'),
  path('cancel_order/<int:order_id>',views.cancel_order,name='cancel_order'),
  path('order/details/<int:order_id>',views.order_details,name='order_details'),
  path('admin_order/details/<int:order_id>',views.admin_order_details,name='admin_order_details'),
  path('razorpay-payment/',views.razorpay_payment, name='razorpay_payment'),
  path('verify-payment/',views.verify_payment, name='verify_payment'),
  path('return/<int:item_id>/',views.request_return, name='request_return'),
  path('returns/',views.manage_returns, name='manage_returns'),
  path('returns/process/<int:item_id>/',views.process_return,name='process_return'),
  path('wallet_payment/<int:final_amount>',views.wallet_payemt,name='wallet_payment')

]