from django.shortcuts import render,get_object_or_404,redirect
from .models import Cart,CartItem,Wishlist
from products.models import Variant,product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json
from coupons.models import Coupon
from django.views.decorators.cache import never_cache
from django.utils import timezone
# Create your views here.
@never_cache
@login_required(login_url='login')
def cart_view(request):
  cart=Cart.objects.filter(user=request.user).first()
  cart_items=cart.cart_item.all() if cart else []
  coupons=Coupon.objects.filter(active=True, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
  context={
    'cart':cart,
    'cart_items': cart_items,
    'discounted_price': cart.get_total_discount(),
    'total': cart.get_total() if cart else 0,
    'available_coupons':coupons,
  }
  return render(request,'user/cart.html',context)

@never_cache
@login_required(login_url='login')
def add_to_cart(request,variant_id):
  Product=get_object_or_404(product,variants=variant_id)
  variant=get_object_or_404(Variant,id=variant_id)

  if not variant.is_in_stock():
    messages.error(request, "This variant is out of stock.")
    return redirect('product_details', product_id=Product.id)

  else:
    cart,created=Cart.objects.get_or_create(user=request.user)

    cart_item,item_created=CartItem.objects.get_or_create(cart=cart,variant=variant)
    if not item_created:
      cart_item.quantity+=1
      cart_item.save()
    return redirect('cart_view')
  

@login_required(login_url='login')
def remove_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.delete()
            cart_total = sum(item.get_subtotal() for item in CartItem.objects.filter(cart__user=request.user))
            cart_empty = not CartItem.objects.filter(cart__user=request.user).exists()
            return JsonResponse({
                'success': True,
                'message': 'Item removed from cart.',
                'total': cart_total,
                'cart_empty': cart_empty
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found in cart.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required(login_url='login')  
def update_cart(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            new_quantity = data.get('quantity')

            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            variant = Variant.objects.get(id=cart_item.variant.id)

            # Validate quantity
            if 1 <= int(new_quantity) <= 3 and int(new_quantity) <= variant.stock:
                cart_item.quantity = int(new_quantity)
                cart_item.save()
            elif int(new_quantity) > variant.stock:
                return JsonResponse({'success': False, 'error': 'Not enough stock available.'})
            elif int(new_quantity) > 3:
                return JsonResponse({'success': False, 'error': 'You can only add up to 3 items.'})
            else:
                cart_item.delete()

            # Calculate totals
            cart_total = sum(item.get_subtotal() for item in CartItem.objects.filter(cart__user=request.user))
            return JsonResponse({
                'success': True,
                'subtotal': cart_item.get_subtotal(),
                'total': cart_total,
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart item not found.'})
        except Variant.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Variant not found.'})
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid quantity.'})

    return JsonResponse({'success': False, 'error': 'Invalid request.'})

@never_cache
@login_required(login_url='login')
def wishlist_view(request):
  wishlist=Wishlist.objects.filter(user=request.user).first()
  if wishlist:
    items=wishlist.variant.all()
  else:
    items=[]
  return render(request,'user/wishlist.html',{'wishlist_items': items})

@login_required(login_url='login')
def add_to_wishlist(request,variant_id):
  if not request.user.is_authenticated:
    messages.error(request, "You need to log in to add items to your wishlist.")
    return redirect('login')

  variant=get_object_or_404(Variant, id=variant_id)

    
  wishlist,created = Wishlist.objects.get_or_create(user=request.user)

  if wishlist.variant.filter(id=variant.id).exists():
    messages.info(request, "This item is already in your wishlist.")
  else:
    wishlist.variant.add(variant)
    messages.success(request, "Item added to your wishlist.")

  return redirect('wishlist')

@login_required(login_url='login')
def remove_from_wishlist(request,variant_id):
  variant=get_object_or_404(Variant,id=variant_id)
  Wishlist.objects.filter(user=request.user,variant=variant).delete()
  messages.success(request,f"{variant.product.name } removed from wishlist")
  return redirect('wishlist')
