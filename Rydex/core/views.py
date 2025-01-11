from django.shortcuts import render
from categories.models import categories
from products.models import product
from django.views.decorators.cache import never_cache


# Create your views here.
@never_cache
def home(request):
  Categories=categories.objects.all()
  products=product.objects.all()
  return render(request,'user/homepage.html',{'categories':Categories, 'products':products})