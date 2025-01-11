from django.urls import path
from . import views

urlpatterns=[
  path('profile/add_profile_pic',views.add_profile_pic,name='add_profile_pic'),
  path('profile/edit_profile_pic',views.edit_profile_pic,name='edit_profile_pic'),
]