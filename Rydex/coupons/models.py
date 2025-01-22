from django.db import models
from user_auth.models import User

# Create your models here.

class Coupon(models.Model):
  code=models.CharField(max_length=50,unique=True)
  discount=models.DecimalField(max_digits=5,decimal_places=2,help_text="percentage discount (e.g. for 10 for 10%)")
  max_discount=models.DecimalField(max_digits=5,decimal_places=2,help_text="maximum discount amount")
  min_order_amount=models.DecimalField(max_digits=6,decimal_places=2,help_text="minimum order value to apply the coupon")
  active=models.BooleanField(default=True)
  valid_from=models.DateTimeField()
  valid_to=models.DateTimeField()

  def __str__(self):
    return self.code
  
  def is_valid(self):
    from django.utils.timezone import now
    return self.active and self.valid_from <=now() <= self.valid_to 
  
class Appliedcoupon(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  coupon=models.ForeignKey(Coupon,on_delete=models.CASCADE)
  applied_at=models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.user} - {self.coupon.code}"
  
