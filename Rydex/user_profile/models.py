from django.db import models
from user_auth.models import User

# Create your models here.

class profile(models.Model):
  user=models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
  profile_picture=models.ImageField(upload_to='profile_pics/',null=True,blank=True)