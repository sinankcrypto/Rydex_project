from django.urls import path,include
from user_auth import views
from core import urls
from .views import CustomViewLogout

urlpatterns= [
  path('',include(urls)),
  path('admin_login/',views.admin_login,name='admin_login'),
  path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
  path('signup',views.user_signup,name='signup'),
  path('login',views.user_login,name='login'),
  path('otp_verification',views.verify_otp_view,name='otp_verification'),
  path('logout/',CustomViewLogout.as_view(),name='logout'),

]