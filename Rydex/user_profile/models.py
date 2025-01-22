from django.db import models
from user_auth.models import User
from order.models import Order

# Create your models here.

class profile(models.Model):
  user=models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
  profile_picture=models.ImageField(upload_to='profile_pics/',null=True,blank=True)
  wallet_balance=models.DecimalField(max_digits=10,decimal_places=2,default=0.0)

  def add_to_wallet(self,amount):
    if amount>0:
      self.wallet_balance+=amount
      self.save()
      
class WalletTransaction(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='wallet_transactions')
  order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
  amount=models.DecimalField(max_digits=10,decimal_places=2)
  transaction_type=models.CharField(max_length=10,choices=[('CREDIT','Credit'),('DEBIT','Debit')])
  created_at=models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.transaction_type} of {self.amount} for {self.user.username}"