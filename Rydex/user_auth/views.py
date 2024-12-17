from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .forms import CustomUserFormCreation
import random
from django.core.mail import send_mail
from user_auth.models import User
from django.views import View
# Create your views here.

@never_cache
def admin_login(request):
  if request.method=="POST":
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=authenticate(request,username=username,password=password)
  
    if user is not None:
      login(request,user)
      if user.is_superuser:
        return redirect('admin_dashboard')
      else:
        messages.error(request,"you are not authorized to access this page")
        return redirect('admin_login')
    else:
      messages.error(request,"invalid username or password")
      return redirect('admin_login')
  return render(request,'admin_login.html')

@never_cache
@login_required(login_url='admin_login')
def admin_dashboard(request):
  return render(request,'admin_dashboard.html')

def user_signup(request):
  if request.method=='POST':
    form=CustomUserFormCreation(request.POST)
    if form.is_valid():
      user=form.save(commit=False)
      user.is_active=False
      user.save()

      otp = generate_otp()
      request.session['otp'] = otp
      request.session['otp_email'] = user.email

      send_otp_email(user.email, otp)

      messages.success(request, "Registration successful. Please verify the OTP sent to your email.")
      return redirect('otp_verification')
    else:
      messages.error(request,'There was an error with your signup. Please try again.')
  else:
    form=CustomUserFormCreation()
  
  return render(request,'signup.html',{'form':form})


def user_login(request):
  if request.method=='POST':
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=authenticate(request,username=username,password=password)

    if user is not None:
      login(request, user)
      return redirect('home')
    
    else:
      messages.error(request,"invalid username or password") 
      return redirect('login')
  return render(request,'login.html')


def generate_otp():
  return str(random.randint(100000,999999))

def send_otp_email(email,otp):
  subject="Your OTP Verification Code"
  message=f"Your OTP is {otp}. It is  valid for 5 minutes."
  from_email="rydexboss@gmail.com"

  send_mail(subject,message,from_email,[email])


def verify_otp_view(request):
  if request.method=='POST':
    entered_otp=request.POST.get('otp')
    
    session_otp=request.POST.get('otp')
    session_email=request.POST.get('otp_email')

    if not session_otp or session_email:
      messages.error(request,"OTP Session expired. Please sign up again")
      return redirect('signup')

    if entered_otp==session_otp:
      user = User.objects.get(email=session_email)  # Use your custom user model
      user.is_active = True  # Activate the user account
      user.save()
      
      
      
      # Clear OTP after successful verification
      del request.session['otp']
      del request.session['otp_email']

      messages.success(request,"OTP Verified Succesfully")
      return redirect('login')
    else:
      messages.error(request,"Invalid OTP. Please try again.")
  return render(request,'otp_verification.html')

class CustomViewLogout(View):
  def get(self,request,*args,**kwargs):
    logout(request)
    return redirect('login')