from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
  Address=models.TextField()
  email=models.EmailField(unique=True)
  
