from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfilePictureForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from user_auth.models import User
from .models import profile
from django.views.decorators.cache import never_cache

# Create your views here.

@login_required
def add_profile_pic(request):
  if request.method=='POST':
    form=ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
    if form.is_valid():
      form.save()
      return redirect('profile')
  return redirect('profile')

@login_required
def edit_profile_pic(request):
  if request.method=='POST':
    form=ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
    if form.is_valid():
      form.save()
      return redirect('profile')
  return redirect('profile')

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs,):
  if created:
    profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
  instance.profile.save()

@login_required(login_url='login')
@never_cache
def wallet_view(request):
  user=request.user
  transactions=user.wallet_transactions.all().order_by('-created_at')
  return render(request,'user/wallet.html',{'user': user, 'transactions': transactions})