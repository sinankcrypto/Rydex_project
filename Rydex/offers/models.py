from django.db import models
from categories.models import categories

# Create your models here.

class CategoryOffer(models.Model):
  category=models.OneToOneField(categories,on_delete=models.CASCADE,related_name='category_offer')
  discount_percentage=models.DecimalField(max_digits=5,decimal_places=2,help_text="percentage discount for this category")
  valid_from=models.DateTimeField()
  valid_to=models.DateTimeField()
  is_active=models.BooleanField(default=True)

  def __str__(self):
    return f"{self.category.name} - {self.discount_percentage}%"
  
  def is_valid(self):
    from django.utils.timezone import now
    return self.is_active and self.valid_from <=now() <= self.valid_to
  
  def save(self,*args,**kwargs):
    super().save(*args,**kwargs)
    if self.is_active:
      self.category.offer=self
    else:
      self.category.offer=None
    self.category.save()
  

  
class ProductOffer(models.Model):
  product=models.OneToOneField('products.product',on_delete=models.CASCADE,related_name='product_offer')
  discount_percentage=models.DecimalField(max_digits=5,decimal_places=2,help_text="percentage discount for this product")
  valid_from=models.DateTimeField()
  valid_to=models.DateTimeField()
  is_active=models.BooleanField(default=True)

  def __str__(self):
    return f"{self.product.name} - {self.discount_percentage}%"

  def is_valid(self):
    from django.utils.timezone import now
    return self.is_active and self.valid_from <=now() <= self.valid_to  
  
  def save(self,*args,**kwargs):
    super().save(*args,**kwargs)
    if self.is_active:
      self.product.offer=self
    else:
      self.product.offer=None
    self.product.save()