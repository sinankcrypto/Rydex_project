from django.db import models
from categories.models import categories
from offers.models import ProductOffer

# Create your models here.

class product(models.Model):
  name=models.CharField(max_length=200)
  description=models.TextField()
  price=models.DecimalField(max_digits=10,decimal_places=2)
  offer=models.OneToOneField(ProductOffer,on_delete=models.SET_NULL,null=True,blank=True,related_name='related_product_offer')
  category=models.ForeignKey(categories,on_delete=models.CASCADE,null=True,blank=True,related_name="products")
  image_main=models.ImageField(upload_to='product_images/')
  image_1=models.ImageField(upload_to='product_images/',null=True,blank=True)
  image_2=models.ImageField(upload_to='product_images/',null=True,blank=True)
  image_3=models.ImageField(upload_to='product_images/',null=True,blank=True)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateField(auto_now=True)
  is_active=models.BooleanField(default=True)

  def __str__(self):
    return self.name
  
  def get_best_discount(self):
    best_discount=0

    if self.offer:
      best_discount=max(best_discount,self.offer.discount_percentage)

    if self.category.offer:
      best_discount=max(best_discount,self.category.offer.discount_percentage)
    
    return best_discount
  
  def get_discounted_price(self):
    best_discount=self.get_best_discount()
    return self.price-(self.price*best_discount/100)
  


class Variant(models.Model):
  SIZE_CHOICES= [
    ('S','Small'),
    ('M','Medium'),
    ('L','Large'),
    ('XL','Extra Large')
  ]
  product=models.ForeignKey(product,on_delete=models.CASCADE,related_name="variants")
  size=models.CharField(max_length=2,choices=SIZE_CHOICES)
  stock=models.PositiveIntegerField(default=0)

  def __str__(self):
    return f"{self.product.name}- {self.size}"
  
  def is_in_stock(self):
    return self.stock > 0
  