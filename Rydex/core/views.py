from django.shortcuts import render
from categories.models import categories
from products.models import product


# Create your views here.

def home(request):
  Categories=categories.objects.all()
  products=product.objects.all()
  return render(request,'user/homepage.html',{'categories':Categories, 'products':products})