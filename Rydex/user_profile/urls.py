from django.urls import path
from user_profile import views

urlpatterns = [
    path('profile/add_profile_pic', views.add_profile_pic, name='add_profile_pic'),
    path('profile/edit_profile_pic', views.edit_profile_pic, name='edit_profile_pic'),
    path('profile/wallet', views.wallet_view, name='wallet_view'),
    path('profile/change-username/', views.change_username, name='change_username'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/change-email/', views.change_email_request, name='change_email_request'),
    path('profile/verify-email-otp/', views.verify_email_change_otp, name='verify_email_change_otp'),
    path('profile/resend-email-otp/', views.resend_email_change_otp, name='resend_email_change_otp'),
]