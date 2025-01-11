from django.shortcuts import render,get_object_or_404,redirect
from .models import Cart,CartItem,Wishlist
from products.models import Variant,product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.

@login_required
def cart_view(request):
  cart=Cart.objects.filter(user=request.user).first()
  cart_items=cart.cart_item.all() if cart else []
  context={
    'cart':cart,
    'cart_items': cart_items,
    'total': cart.get_total() if cart else 0
  }
  return render(request,'user/cart.html',context)

@login_required
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

@login_required
def remove_cart_item(request,item_id):
  cart_item=get_object_or_404(CartItem,id=item_id,cart__user=request.user)
  cart_item.delete()
  return redirect('cart_view')
  
def update_cart(request):
  if request.method=='POST':
    for key,value in request.POST.items():
      if key.startswith("quantity_"):
        cart_item_id=key.split("_")[1]
        try:
          cart_item=CartItem.objects.get(id=cart_item_id,cart__user=request.user)
          new_quantity=int(value)
          variant=Variant.objects.get(id=cart_item.variant.id)
          if 4>new_quantity>0 and variant.stock>new_quantity:
            cart_item.quantity=new_quantity
            cart_item.save()
          elif new_quantity > variant.stock:
            messages.error(request,"not enough stock")

          elif new_quantity > 3:
            messages.error(request,"can only add up to 3 quantity")
            
          else:
            cart_item.delete()

        except CartItem.DoesNotExist:
          messages.error(request,"Cart item not found.")
    messages.success(request,"Cart updated succesfully.")
    return redirect("cart_view")
  return redirect("cart_view")

@login_required
def wishlist_view(request):
  wishlist=Wishlist.objects.filter(user=request.user).first()
  if wishlist:
    items=wishlist.variant.all()
  else:
    items=[]
  return render(request,'user/wishlist.html',{'wishlist_items': items})

@login_required
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

@login_required
def remove_from_wishlist(request,variant_id):
  variant=get_object_or_404(Variant,id=variant_id)
  Wishlist.objects.filter(user=request.user,variant=variant).delete()
  messages.success(request,f"{variant.product.name } removed from wishlist")
  return redirect('wishlist')
