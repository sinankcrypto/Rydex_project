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
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.db.models import Sum, Count,Case,When,F
from order.models import Order,order_item
from django.db.models.functions import ExtractDay,ExtractMonth,ExtractHour
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe


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
  return render(request,'admin/admin_login.html',)

def admin_dashboard(request):
    filter_type = request.GET.get('filter', 'daily')
    today = datetime.today()

    if filter_type == 'yearly':
        orders = (
            Order.objects.filter(created_at__year=today.year)
            .annotate(month=ExtractMonth('created_at'))
            .values('month')
            .annotate(
                amount=Sum('final_amount'),
                order_count=Count('id')
            )
            .order_by('month')
        )
        orders_data = [
            {
                'created_at': f"{today.year}-{order['month']:02d}-01",
                'amount': float(order['amount'])
            }
            for order in orders
        ]

    elif filter_type == 'monthly':
        orders = (
            Order.objects.filter(
                created_at__year=today.year,
                created_at__month=today.month
            )
            .annotate(day=ExtractDay('created_at'))
            .values('day')
            .annotate(
                amount=Sum('final_amount'),
                order_count=Count('id')
            )
            .order_by('day')
        )
        orders_data = [
            {
                'created_at': f"{today.year}-{today.month:02d}-{order['day']:02d}",
                'amount': float(order['amount'])
            }
            for order in orders
        ]

    else:  # Daily
        orders = (
            Order.objects.filter(created_at__date=today.date())
            .annotate(hour=ExtractHour('created_at'))
            .values('hour')
            .annotate(
                amount=Sum('final_amount'),
                order_count=Count('id')
            )
            .order_by('hour')
        )
        orders_data = [
            {
                'created_at': f"{today.date()} {order['hour']:02d}:00",
                'amount': float(order['amount'])
            }
            for order in orders
        ]

    # Properly serialize the data and mark it as safe
    orders_json = mark_safe(json.dumps(orders_data, cls=DjangoJSONEncoder))
    
    top_products = (
        order_item.objects.values(
            'variant__product__name',
            'variant__product__category__name'
        )
        .annotate(
            total_quantity=Sum('quantity'),
            total_sales=Sum(
                Case(
                    When(
                        offer_price__isnull=False,
                        then=F('offer_price') * F('quantity')
                    ),
                    default=F('price') * F('quantity')
                )
            )
        )
        .order_by('-total_quantity')[:10]
    )

    top_categories = (
        order_item.objects.values(
            'variant__product__category__name'
        )
        .annotate(
            total_sales=Sum(
                Case(
                    When(
                        offer_price__isnull=False,
                        then=F('offer_price') * F('quantity')
                    ),
                    default=F('price') * F('quantity')
                )
            ),
            total_items=Sum('quantity')
        )
        .order_by('-total_sales')[:10]
    )

    context = {
        'orders': orders_json,
        'filter_type': filter_type,
        'top_products': top_products,
        'top_categories': top_categories,
    }
    return render(request, 'admin/admin_dashboard.html', context)

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
  
  return render(request,'accounts/signup.html',{'form':form})

@never_cache
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

  return render(request,'accounts/login.html')


def generate_otp():
  return str(random.randint(100000,999999))

def send_otp_email(email,otp):
  subject="Your OTP Verification Code"
  message=f"Your OTP is {otp}. It is  valid for 5 minutes."
  from_email="rydexboss@gmail.com"

  send_mail(subject,message,from_email,[email])

def resend_otp_view(request):
    if request.method == 'POST':
        email = request.session.get('otp_email')  
        if not email:
            messages.error(request, "Session expired. Please sign up again.")
            return redirect('signup')

        try:
            user = User.objects.get(email=email)
            if user.is_active:
                messages.info(request, "Account is already verified.")
                return redirect('login')

            otp = generate_otp()
            request.session['otp'] = otp

            send_otp_email(email, otp)

            messages.success(request, "A new OTP has been sent to your email.")
            return redirect('otp_verification')
        except User.DoesNotExist:
            messages.error(request, "User not found. Please sign up again.")
            return redirect('signup')
    else:
        return redirect('signup')


def verify_otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')  
        session_email = request.session.get('otp_email')  
        
        if not session_otp or not session_email:
            messages.error(request, "OTP session expired. Please sign up again.")
            return redirect('signup')

        if entered_otp == session_otp:
            try:
               
                user = User.objects.get(email=session_email)
                user.is_active = True
                user.save()

                request.session.pop('otp', None)
                request.session.pop('otp_email', None)

                messages.success(request, "OTP verified successfully! Your account is now active.")
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
            except User.DoesNotExist:
                messages.error(request, "No user found with the provided email.")
                return redirect('signup')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'registration/otp_verification.html')

class CustomViewLogout(View):
  def get(self,request,*args,**kwargs):
    logout(request)
    return redirect('login')
  
