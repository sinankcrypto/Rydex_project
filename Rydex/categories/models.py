from django.db import models

# Create your models here.

class categories(models.Model):
  name=models.CharField(max_length=255,unique=True)
  description=models.TextField(null=True,blank=True)
  image=models.ImageField(upload_to='categories/',null=True,blank=True)
  is_listed=models.BooleanField(default=True)
  created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
  updated_at=models.DateTimeField(auto_now=True)
  offer=models.OneToOneField(
    'offers.CategoryOffer',
    on_delete=models.SET_NULL,
    null=True,blank=True,
    related_name='related_category_offer'
  )


  def __str__(self):
    return self.name