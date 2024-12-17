from django.shortcuts import render,redirect,get_object_or_404
from .models import product
from .forms import productform
from categories.models import categories

# Create your views here.

def product_list(request):
  products=product.objects.all()
  return render(request,'admin_products.html',{'products':products})

def add_product(request):
  if request.method=='POST':
    form=productform(request.POST,request.FILES)
    if form.is_valid:
      form.save()
      return redirect('product_list')
  else:
    form=productform()
  Categories=categories.objects.all()
  return render(request,'admin_products_add.html',{'form':form ,'categories': Categories})

def edit_product(request,product_id):
  Product=get_object_or_404(product,id=product_id)

  if request.method=='POST':
    form=productform(request.POST,request.FILES,instance=Product)
    if form.is_valid():
      form.save()
      return redirect('product_list')
  else:
    form=productform(instance=Product)

  Categories=categories.objects.all()
  return render(request,'admin_products_edit.html',
                {'form': form, 'categories': Categories, 'product': Product})  

def productDetails(request,product_id):
  Product=get_object_or_404(product,id=product_id)
  
  return render(request,'user/product_details.html',{'product':Product})


