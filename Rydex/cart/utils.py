from .models import Cart

def get_cart(user):
  if user.is_authenticated:
    cart,created=Cart.objects.get_or_create(user=user)
    return cart
  return None
