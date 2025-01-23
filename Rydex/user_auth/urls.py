from django.urls import path,include
from user_auth import views
from core import urls
from .views import CustomViewLogout
from django.contrib.auth import views as auth_views
from . import views

urlpatterns= [
  path('',include(urls)),
  path('admin_login/',views.admin_login,name='admin_login'),
  path('signup',views.user_signup,name='signup'),
  path('login/',views.user_login,name='login'),
  path('otp_verification',views.verify_otp_view,name='otp_verification'),
  path('logout/',CustomViewLogout.as_view(),name='logout'),

  path('password-reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
  path('password-reset/done',
       auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
       name='password_reset_done'),
  path('reset/<uidb64>/<token>/',
       auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
       name='password_reset_confirm'),
  path('reset/done/',
       auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
       name='password_reset_complete'),
  path('accounts/',include('allauth.urls')),
  path('resend_otp/',views.resend_otp_view,name='resend_otp'),

]