from django.db import models
from categories.models import categories

# Create your models here.

class product(models.Model):
  name=models.CharField(max_length=200)
  description=models.TextField()
  price=models.DecimalField(max_digits=10,decimal_places=2)
  category=models.ForeignKey(categories,on_delete=models.CASCADE,null=True,blank=True)
  image_main=models.ImageField(upload_to='product_images/')
  image_1=models.ImageField(upload_to='product_images/',null=True,blank=True)
  image_2=models.ImageField(upload_to='product_images/',null=True,blank=True)
  image_3=models.ImageField(upload_to='product_images/',null=True,blank=True)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateField(auto_now=True)

  def __str__(self):
    return self.name
  