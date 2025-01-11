from django.db import models
from user_auth.models import User
from products.models import Variant

# Create your models here.

class Cart(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  created_at=models.DateTimeField(auto_now_add=True)

  def get_total(self):
    return sum(item.get_subtotal() for item in self.cart_item.all())
  
  def __str__(self):
    return f"Cart- {self.user.username}"
  
class CartItem(models.Model):
  cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_item')
  variant=models.ForeignKey(Variant,on_delete=models.CASCADE)
  quantity=models.PositiveIntegerField(default=1)

  def get_subtotal(self):
    return self.variant.product.price*self.quantity
  
  def __str__(self):
    return f"{self.variant.product.name}- {self.quantity}"

class Wishlist(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  variant=models.ManyToManyField(Variant,related_name='wishlists')
  added_at=models.DateTimeField(auto_now_add=True)
