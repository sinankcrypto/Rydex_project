from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Coupon,Appliedcoupon
from django.utils.timezone import now
from django.http import JsonResponse
import json
from .forms import CouponForm
from cart.utils import get_cart


# Create your views here.

def coupon_list(request):
  coupons=Coupon.objects.all()
  return render(request,'admin/coupon_list.html',{'coupons': coupons})

def add_coupon(request):
  if request.method=='POST':
    form=CouponForm(request.POST) 
    if form.is_valid():
      form.save()
      messages.error(request,'Coupon added succesfully.')
      return redirect('coupon_list')
    else:
      print(form.errors)
      messages.error(request,'form not valid')
  else:
    form=CouponForm
  return render(request,'admin/coupon_form.html',{'form': form , 'title': 'add_coupon'})

def edit_coupon(request,coupon_id):
  coupon=get_object_or_404(Coupon,id=coupon_id)
  if request.method=='POST':
    form=CouponForm(request.POST,instance=coupon)
    if form.is_valid():
      form.save()
      messages.success(request,'Coupon updated succesfully! ')
      return redirect('coupon_list')
  else:
    form=CouponForm(instance=coupon)
  return render(request,'admin/coupon_form.html',{'form': form, 'title': 'Edit Coupon'})

def coupon_delete(request,coupon_id):
  coupon=get_object_or_404(Coupon,id=coupon_id)
  coupon.delete()
  messages.success(request,'Coupon deleted succesfully')
  return redirect('admin_coupon_list')
    
def apply_coupon(request):
    
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
      print(f"x-requested-with header: {request.headers.get('x-requested-with')}")
      data = json.loads(request.body)
      coupon_code = data.get('coupon_code', '').strip()
      cart = get_cart(request.user)

      if not coupon_code:
        return JsonResponse({'success': False, 'error': 'Coupon code is required'})

      try:
        coupon = get_object_or_404(Coupon, code=coupon_code, active=True)
        print(f"Coupon code received: {data.get('coupon_code', '').strip()}")
        if coupon.is_valid():
          if cart.get_total() >= coupon.min_order_amount:
            discount = min(coupon.discount / 100 * cart.get_total(), coupon.max_discount)
            total = cart.get_total() - discount
            request.session['discounted_total'] = float(total)
            return JsonResponse({
              'success': True,
              'message': f"Coupon applied! You saved ₹{discount:.2f}.",
              'total': f"{total:.2f}"
            })
          else:
            return JsonResponse({'success': False, 'error': 'Cart total is below the minimum order amount.'})
        else:
          return JsonResponse({'success': False, 'error': 'Coupon is expired.'})
      except Coupon.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid coupon code.'})

    # Handle invalid request methods or headers
    return JsonResponse({'success': False, 'error': 'Invalid request.'})