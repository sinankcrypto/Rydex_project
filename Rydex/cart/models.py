from django.db import models
from user_auth.models import User
from products.models import Variant

# Create your models here.

class Cart(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  created_at=models.DateTimeField(auto_now_add=True)

  def get_total_discount(self):
    return sum(
      (item.variant.product.price-item.get_discounted_price())*item.quantity
      for item in self.cart_item.all()
    )

  def get_total(self):
    return sum(item.get_subtotal() for item in self.cart_item.all())
  
  def __str__(self):
    return f"Cart- {self.user.username}"
  
class CartItem(models.Model):
  cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_item')
  variant=models.ForeignKey(Variant,on_delete=models.CASCADE)
  quantity=models.PositiveIntegerField(default=1)

  def get_best_discount(self):
    best_discount=0
    if hasattr(self.variant.product,'offer') and self.variant.product.offer and self.variant.product.offer.is_active:
      if self.variant.product.offer.is_valid():
        best_discount=self.variant.product.offer.discount_percentage

    if hasattr(self.variant.product.category,'offer') and self.variant.product.category.offer and self.variant.product.category.offer.is_active:
      if self.variant.product.category.offer.is_valid():
        best_discount=max(best_discount,self.variant.product.category.offer.discount_percentage)
    return best_discount
  
  def get_discounted_price(self):
    discount_percentage=self.get_best_discount()
    discounted_price=self.variant.product.price-(self.variant.product.price*discount_percentage/100)
    return discounted_price

  def get_subtotal(self):
    return self.get_discounted_price()*self.quantity
  
  def __str__(self):
    return f"{self.variant.product.name}- {self.quantity}"

class Wishlist(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  variant=models.ManyToManyField(Variant,related_name='wishlists')
  added_at=models.DateTimeField(auto_now_add=True)
