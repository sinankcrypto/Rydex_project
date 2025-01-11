from django.shortcuts import render,redirect,get_object_or_404
from .models import product,Variant
from .forms import productform,Variantform
from categories.models import categories
from django.db.models import Q

# Create your views here.

def product_list(request):
  products=product.objects.all()
  return render(request,'admin/admin_products.html',{'products':products})

def toggle_product_status(request,product_id):
  if request.method=='POST':
    Product=get_object_or_404(product,id=product_id)
    Product.is_active= not Product.is_active
    Product.save()
  return redirect('product_list')


def add_product(request):
  if request.method=='POST':
    form=productform(request.POST,request.FILES)
    if form.is_valid:
      form.save()
      return redirect('product_list')
  else:
    form=productform()
  Categories=categories.objects.all()
  return render(request,'admin/admin_products_add.html',{'form':form ,'categories': Categories})

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
  return render(request,'admin/admin_products_edit.html',
                {'form': form, 'categories': Categories, 'product': Product})  

def productDetails(request,product_id):
  Product = get_object_or_404(product, id=product_id)
    
    # Get the selected size from the request or default to 'M'
  selected_size = request.GET.get('size', 'M')
    
    # Get the variant for the selected size
  variant = Product.variants.filter(size=selected_size).first()
    
  return render(request, 'user/product_details.html', {
        'product': Product,
        'variant': variant
    })


def variant_list(request,product_id):
  Product=get_object_or_404(product,id=product_id)
  variants=Product.variants.all()
  return render(request,'admin/variant_list.html',{'product': Product,'variants':variants})

def add_variant(request,product_id):
  Product=get_object_or_404(product,id=product_id)
  if request.method=='POST':
    form=Variantform(request.POST)
    if form.is_valid():
      variant=form.save(commit=False)
      variant.product=Product
      variant.save()
      return redirect('variant_list',product_id=Product.id)
  else:
    form=Variantform()
  return render(request,'admin/add_variant.html',{'form':form,'product':Product})

def edit_variant(request,Variant_id):
  variant=get_object_or_404(Variant,id=Variant_id)
  if request.method=='POST':
    form=Variantform(request.POST,instance=variant)
    if form.is_valid():
      form.save()
      return redirect('variant_list',product_id=variant.product.id)
  else:
    form=Variantform(instance=variant)
  return render(request,'admin/edit_variant.html',{'form':form, 'variant': variant})

def all_products(request):
  
  products=product.objects.all()

  search_query=request.GET.get('search', '')
  if search_query:
    products=product.objects.filter(
      Q(name__icontains=search_query)| Q(description__icontains=search_query)
    )

  min_price=request.GET.get('min_price','')
  max_price=request.GET.get('max_price','')
  if min_price:
    products=products.filter(price__gte=min_price)

  if max_price:
    products=products.filter(price__lte=max_price)

  sort_option=request.GET.get('sort', '')
  
  if sort_option=='price_asc':
    products=products.order_by('price')
  elif sort_option=='price_desc':
    products=products.order_by('-price')
  elif sort_option=='name_asc':
    products=products.order_by('name')
  elif sort_option=='name_desc':
    products=products.order_by('-name')

  return render(request,'user/all_products.html',{'products': products})
