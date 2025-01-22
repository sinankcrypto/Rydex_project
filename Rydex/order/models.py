from django.db import models
from user_auth.models import User
import uuid
from products.models import Variant

# Create your models here.

class Address(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  full_name=models.CharField(max_length=100)
  phone_number=models.CharField(max_length=15)
  address_line=models.TextField()
  city=models.CharField(max_length=50)
  state=models.CharField(max_length=50)
  pin_code=models.CharField(max_length=10)
  created_at=models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.full_name}, {self.city}"
  
class Order(models.Model):
  STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('SHIPPED', 'Shipped'),
    ('DELIVERED', 'Delivered'),
    ('CANCELLED', 'Cancelled'),
  ]
  PAYMENT_METHODS=[
    ('COD','Cash On Delivery'),
    ('RAZORPAY','Razorpay'),
    ('WALLET','Wallet')
  ]
  PAYMENT_STATUS_CHOICES=[
    ('PAID','Paid'),
    ('FAILED','Failed')
  ]
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  address=models.ForeignKey(Address,on_delete=models.CASCADE,related_name='orders')
  created_at=models.DateTimeField(auto_now_add=True)
  status=models.CharField(max_length=15,choices=STATUS_CHOICES)
  tracking_id=models.CharField(max_length=8,unique=True,blank=True)
  amount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
  payment_method=models.CharField(max_length=10,choices=PAYMENT_METHODS,default='COD')
  final_amount=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
  payment_status=models.CharField(max_length=15,choices=PAYMENT_STATUS_CHOICES,default='FAILED')
  payment_id=models.CharField(max_length=20,null=True,blank=True)

  

  def save(self,*args,**kwargs):
    if not self.tracking_id:
      self.tracking_id=str(uuid.uuid4())[:8].upper()

    super().save(*args,**kwargs)
  def __str__(self):
    return f"Order #{self.id} - {self.status}"
  
  
class order_item(models.Model):
  class ReturnStatus(models.TextChoices):
        REQUESTED = 'Requested', 'Requested'
        APPROVED = 'Approved', 'Approved'
        REJECTED = 'Rejected', 'Rejected'
        NOT_REQUESTED = 'Not Requested', 'Not Requested'

  order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
  variant=models.ForeignKey(Variant,on_delete=models.CASCADE)
  quantity=models.PositiveIntegerField()
  price=models.DecimalField(max_digits=10,decimal_places=2)
  offer_price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
  return_requested = models.BooleanField(default=False)
  return_reason = models.TextField(null=True, blank=True)
  return_status = models.CharField(
        max_length=20,
        choices=ReturnStatus.choices,
        default=ReturnStatus.NOT_REQUESTED,
    )

  def get_subtotal(self):
    return self.offer_price*self.quantity if self.offer_price else self.variant.product.price*self.quantity

