from django.shortcuts import render,redirect,get_object_or_404
from .forms import AddressForm
from django.contrib.auth.decorators import login_required
from .models import Address,Order,order_item
from django.http import HttpResponseForbidden
from django.contrib import messages
from cart.models import Cart
from django.db import transaction
from products.models import Variant

# Create your views here.

@login_required
def add_address(request):
  next_page=request.GET.get('next','payment')
  if request.method=='POST':
    form=AddressForm(request.POST)
    if form.is_valid():
      address=form.save(commit=False)
      address.user=request.user
      address.save()
      return redirect(next_page)
  else:
    form=AddressForm()
  return render(request,'user/add_address.html',{'form':form})
  
def payment(request):
  if request.method=='POST':
    address_id=request.POST.get('address')
    address=get_object_or_404(Address,id=address_id,user=request.user)
    user=request.user
    cart = Cart.objects.filter(user=user).first()
    amount = cart.get_total()

    order=Order.objects.create(
      user=request.user,
      address=address,
      status='PENDING',
      amount=amount)
    
    for cart_item in cart.cart_item.all():
      order.items.create(
        variant=cart_item.variant,
        quantity=cart_item.quantity,
        price=cart_item.variant.product.price,
      )

      variant=Variant.objects.get(id=cart_item.variant.id)
      variant.stock-=cart_item.quantity
      variant.save()

    cart.cart_item.all().delete()
    return redirect('success',order_id=order.id)
  
  address=Address.objects.filter(user=request.user)
  return render(request,'user/payment.html',{'addresses':address})

def success(request,order_id):
  order=get_object_or_404(Order,id=order_id,user=request.user)
  return render(request,'user/success.html',{'order':order})

def order_list(request):
  orders=Order.objects.all().order_by('-created_at')
  return render(request,'admin/order_list.html',{'orders':orders})

def update_order_status(request,order_id):
  if request.method=='POST':
    order=get_object_or_404(Order,id=order_id)
    if not request.user.is_staff and request.user != order.user:
      return HttpResponseForbidden("You are not allowed to update this order.")
    
    new_status=request.POST.get('status')
    if order.status == "DELIVERED":
      messages.error(request, "No further changes allowed after delivery.")
    else:
      order.status = new_status
      order.save()
      messages.success(request, f"Order status updated to {new_status}.")
  
  return redirect('order_list')

@login_required()
def edit_address(request,address_id):
  address=get_object_or_404(Address,id=address_id,user=request.user)

  if request.method=='POST':
    form=AddressForm(request.POST,instance=address)
    if form.is_valid():
      form.save()
      return redirect('profile')
  else:
    form=AddressForm(instance=address)

  return render(request,'user/edit_address.html', {'form': form})

def delete_address(request,address_id):
  address=get_object_or_404(Address,id=address_id,user=request.user)
  address.delete()
  messages.success(request,"Address deleted succesfully.")
  return redirect('profile')

def user_orders(request):
  orders=Order.objects.filter(user=request.user).order_by('-created_at')
  return render(request,'user/user_orders.html',{'orders': orders})

def cancel_order(request,order_id):
  order=get_object_or_404(Order,id=order_id,user=request.user)
  order_items=order.items.all()

  if order.status=='PENDING':
    order.status='CANCELLED'
    order.save()

    for order_item in order_items:
      variant=Variant.objects.get(id=order_item.variant.id)
      variant.stock+=order_item.quantity
      variant.save()
    
    messages.success(request,f"Order {order.tracking_id} has been cancelled")
  else:
    messages.error(request,"this order cannot be cancelled.")

  return redirect('user_orders')

def order_details(request,order_id):
  order=get_object_or_404(Order,id=order_id,user=request.user)
  return render(request,'user/order_details.html',{'order':order})