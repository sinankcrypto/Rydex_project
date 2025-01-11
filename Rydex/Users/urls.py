from django.urls import path,include
from core import urls
from . import views

urlpatterns= [

  path('',include(urls)),
  path('admin_dashboard/users',views.Users_page,name='users_page'),
  path('profile',views.profile,name='profile'),


]