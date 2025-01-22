from django.shortcuts import render
from categories.models import categories
from products.models import product
from django.views.decorators.cache import never_cache


# Create your views here.
@never_cache
def home(request):
  Categories=categories.objects.all()
  products=product.objects.select_related('category','offer','product_offer').exclude(is_active=False)
  new_arrivals = product.objects.select_related('category','offer','product_offer').order_by('-created_at').exclude(is_active=False)[:4]
  context={
    'categories':Categories, 
    'products':products, 
    'new_arrivals': new_arrivals
  }
  return render(request,'user/homepage.html',context)