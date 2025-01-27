from django.shortcuts import render,redirect,get_object_or_404
from .forms import AddressForm,ReturnRequestForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Address,Order,order_item
from django.http import HttpResponseForbidden,HttpResponse,JsonResponse
from django.contrib import messages
from cart.models import Cart
from django.db import transaction
from products.models import Variant
from user_profile.models import WalletTransaction
from django.views.decorators.cache import never_cache
from django.conf import settings 
import razorpay
from django.template.loader import get_template
from xhtml2pdf import pisa



# Create your views here.


@login_required(login_url='login')
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
@never_cache
@login_required(login_url='login') 
def payment(request):
  if request.method=='POST':
    address_id=request.POST.get('address')
    payment_method=request.POST.get('payment_method')
    address=get_object_or_404(Address,id=address_id,user=request.user)
    user=request.user
    cart = Cart.objects.filter(user=user).first()
    discounted_total = request.session.get('discounted_total', cart.get_total())
    amount = cart.get_original_total()

    request.session['selected_address'] = address_id
    request.session['payment_method'] = payment_method

    
    if payment_method == "RAZORPAY":
      # Calculate total amount dynamically based on the user's cart or order
      total_amount = discounted_total  # In paise (₹1 = 100 paise)
      total_amount_in_paise = int(total_amount * 100)  # Convert to paise (e.g., ₹500 -> 50000 paise)

      client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
      order = client.order.create({
        "amount": total_amount_in_paise,
        "currency": "INR",
        "payment_capture": 1
      })

      print(order)
      #checking if the id's are equal
      razorpay_order_id = order['id']
      print(razorpay_order_id)
      request.session['razorpay_order_id'] = razorpay_order_id

      # Pass the dynamic order details to Razorpay payment page
      return render(request, "user/razorpay_payment.html", {
        "razorpay_order_id": order["id"],
        "amount": total_amount_in_paise,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "address_id": address_id
      })
    elif payment_method=='WALLET':
      return redirect('wallet_payment', final_amount=int(discounted_total))
    else:
      if amount<=1000:
        order=Order.objects.create(
        user=request.user,
        address=address,
        payment_method=payment_method,
        status='PENDING',
        amount=amount,
        final_amount=discounted_total)
      
        for cart_item in cart.cart_item.all():
          order.items.create(
          variant=cart_item.variant,
          quantity=cart_item.quantity,
          price=cart_item.variant.product.price,
          offer_price=cart_item.variant.product.get_discounted_price()
          )

        variant=Variant.objects.get(id=cart_item.variant.id)
        variant.stock-=cart_item.quantity
        variant.save()

        cart.cart_item.all().delete()
        return redirect('success',order_id=order.id)
      
      else:
        messages.error(request,"Cash On Delivery is not available for orders of amount greater than 1000")
  
  address=Address.objects.filter(user=request.user)
  return render(request,'user/payment.html',{'addresses':address})

@never_cache
@login_required(login_url='login')
def success(request,order_id):
  order=get_object_or_404(Order,id=order_id,user=request.user)
  return render(request,'user/success.html',{'order':order})

@login_required(login_url='login')
def order_list(request):
  orders=Order.objects.all().order_by('-created_at')
  return render(request,'admin/order_list.html',{'orders':orders})

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@never_cache
@login_required(login_url='login')
def delete_address(request,address_id):
  address=get_object_or_404(Address,id=address_id,user=request.user)
  address.delete()
  messages.success(request,"Address deleted succesfully.")
  return redirect('profile')

@login_required(login_url='login')
def user_orders(request):
  orders=Order.objects.filter(user=request.user).order_by('-created_at')
  return render(request,'user/user_orders.html',{'orders': orders})

@never_cache
@login_required(login_url='login')
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

    if order.payment_method=='RAZORPAY':
      order.user.profile.add_to_wallet(order.amount)

      WalletTransaction.objects.create(
        user=order.user,
        order=order,
        amount=order.amount,
        transaction_type='CREDIT',
      )
      messages.success(request,"Refund added to your wallet.")
  else:
    messages.error(request,"this order cannot be cancelled.")

  return redirect('user_orders')

#return order view
@login_required(login_url='login')
@never_cache
def request_return(request,item_id):
  item=get_object_or_404(order_item,id=item_id)

  if request.method=='POST':
    form=ReturnRequestForm(request.POST)
    if form.is_valid():
      reason = form.cleaned_data['reason']
      item.return_requested = True
      item.return_reason = reason
      item.return_status = 'Pending'
      item.save()
      messages.success(request, 'Return request submitted successfully.')
      return redirect('user_orders')
  else:
    form = ReturnRequestForm()

  return render(request,'user/request_return.html',{'form': form, 'item': item})

@login_required(login_url='admin_login')
@staff_member_required
@never_cache
def manage_returns(request):
  return_items = order_item.objects.filter(return_requested=True).order_by('-id')

  return render(request,'admin/return_handling.html',{'return_items': return_items})

@login_required(login_url='admin_login')
@staff_member_required
def process_return(request, item_id):
  item = get_object_or_404(order_item, id=item_id)
  user=item.order.user
  if request.method == 'POST':
    action = request.POST.get('action')
    if action == 'approve':
      item.return_status = 'Approved'
      item.save()
      messages.success(request, f"Return for {item.variant.product.name} has been approved.")
      if item.offer_price:
        price=item.offer_price
      else:
        price=item.price
      user.profile.add_to_wallet(price)

      WalletTransaction.objects.create(
        user=item.order.user,
        order=item.order,
        order_item=item,
        amount=price,
        transaction_type='CREDIT',
      )
    elif action == 'reject':
      item.return_status = 'Rejected'
      item.save()
      messages.warning(request, f"Return for {item.variant.product.name} has been rejected.")
  
  return redirect('manage_returns')


@login_required(login_url='login')
def order_details(request,order_id):
  order=get_object_or_404(Order,id=order_id,user=request.user)
  return render(request,'user/order_details.html',{'order':order})

@staff_member_required
def admin_order_details(request,order_id):
  order=get_object_or_404(Order,id=order_id)
  return render(request,'admin/order_details.html',{'order':order})

@login_required(login_url='login')
@never_cache
def process_refund(request,order_id):
    order=Order.objects.get(id=order_id,user=request.user)
    if order.status in ['CANCELLED','RETURNED']:
      messages.error(request,"Refund already processed for this order")
      return redirect('order_details',order_id=order_id)
    
    if order.payment_method=='COD' and order.status=='CANCELLED':
      messages.error("Cash on delivery orders are not eligible for refund")
      
    else:
      order.user.profile.add_to_wallet(order.amount)

      WalletTransaction.objects.create(
        user=order.user,
        order=order,
        amount=order.amount,
        transaction_type='CREDIT',
      )
      messages.success(request,"Refund added to your wallet.")

def razorpay_payment(request):
  if request.method=='POST':
    amount=int(request.POST.get("amount"))(*100)

    client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    order=client.order.create({
      "amount":amount,
      "currency": "INR",
      "payment_capture": 1  # Auto-capture after payment
    })

    context = {
      "razorpay_order_id": order["id"],
      "amount": amount,
      "razorpay_key_id": settings.RAZORPAY_KEY_ID,
    }
    return render(request, "user/razorpay_payment.html", context)
  
  return render(request, "user/razorpay_payment.html")

def verify_payment(request):
  if request.method == "POST":
    payment_id = request.POST.get("razorpay_payment_id")
    order_id = request.POST.get("razorpay_order_id")
    signature = request.POST.get("razorpay_signature")

    print("Verify payment view called!")
    print(request.POST)

    # Create a Razorpay client instance
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Prepare data to verify the payment
    params_dict = {
      'razorpay_order_id': order_id,
      'razorpay_payment_id': payment_id,
      'razorpay_signature': signature
    }
    original_order_id = request.session.get('razorpay_order_id')
    if order_id != original_order_id:
      print(f"Order ID Mismatch: Received {order_id}, Expected {original_order_id}")
      messages.error(request, "Order ID mismatch. Payment verification failed.")
      return redirect("payment")

    try:
      # Verify the payment signature
      client.utility.verify_payment_signature(params_dict)

      # Retrieve data from the session
      address_id = request.session.get('selected_address')
      payment_method = request.session.get('payment_method')

      

      if not address_id or not payment_method:
        messages.error(request, "Payment verification failed due to missing information.")
        return redirect("payment")

      # Retrieve address and user cart
      address = get_object_or_404(Address, id=address_id, user=request.user)
      user = request.user
      cart = Cart.objects.filter(user=user).first()

      if not cart or not cart.cart_item.exists():
        messages.error(request, "Your cart is empty. Please add items to proceed.")
        return redirect("cart_view")

      discounted_total = request.session.get('discounted_total', cart.get_total())
      amount = cart.get_original_total()

      order = Order.objects.create(
        user=user,
        address=address,
        status='PENDING',
        payment_method=payment_method,
        payment_status='PAID',
        amount=amount,
        final_amount=discounted_total,
        payment_id=payment_id
      )

      for item in cart.cart_item.all():
        order_item.objects.create(order=order, variant=item.variant, 
          quantity=item.quantity,price=item.variant.product.price,
          offer_price= item.get_discounted_price())

            
      cart.cart_item.all().delete()

            
      request.session.pop('selected_address', None)
      request.session.pop('payment_method', None)
      request.session.pop('discounted_total', None)

            
      messages.success(request, "Payment successful! Your order has been placed.")
      return redirect("success",order_id=order.id)  

    except razorpay.errors.SignatureVerificationError:
      messages.error(request, "Payment verification failed. Please try again.")
      return redirect("payment")

  return JsonResponse({"error": "Invalid request method."}, status=400)

def wallet_payemt(request,final_amount):
  user=request.user
  wallet_balance=user.profile.wallet_balance
  cart = Cart.objects.filter(user=user).first()
  address_id=request.session.get('selected_address')
  address=get_object_or_404(Address,id=address_id)

  if wallet_balance>=final_amount:
    order=Order.objects.create(
      user=request.user,
      address=address,
      payment_method="WALLET",
      status='PENDING',
      payment_status='PAID',
      amount=cart.get_original_total(),
      final_amount=final_amount)
    
    user.profile.pay_from_wallet(final_amount)
    
    WalletTransaction.objects.create(
        user=user,
        order=order,
        amount=final_amount,
        transaction_type='DEBIT',
      )

    
    for cart_item in cart.cart_item.all():
      order.items.create(
        variant=cart_item.variant,
        quantity=cart_item.quantity,
        price=cart_item.variant.product.price,
        offer_price=cart_item.variant.product.get_discounted_price()
        )

      variant=Variant.objects.get(id=cart_item.variant.id)
      variant.stock-=cart_item.quantity
      variant.save()

    cart.cart_item.all().delete()
    return redirect('success',order_id=order.id)
  
  else:
    messages.error(request,"not enough balance in your wallet, choose another payment method")
    return redirect('cart_view')

def generate_invoice(request,order_id):
  order=get_object_or_404(Order,id=order_id,user=request.user)
  template_path='user/invoice.html'
  context={'order': order}

  template=get_template(template_path)
  html=template.render(context)

  response=HttpResponse(content_type='application/pdf')
  response['Content-Disposition']= f'attachment; filename="invoice_{order.id}.pdf"'

  pisa_status = pisa.CreatePDF(html, dest=response)

  if pisa_status.err:
    return HttpResponse('Error generating PDF', status=500)
  
  return response
