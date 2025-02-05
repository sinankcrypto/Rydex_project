from django.shortcuts import render,redirect,get_object_or_404
from .models import product,Variant
from .forms import ProductForm,VariantForm
from categories.models import categories
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

# Create your views here.

@never_cache
@staff_member_required
def product_list(request):
  products=product.objects.select_related('category', 'offer').all()
  return render(request,'admin/admin_products.html',{'products':products})

@never_cache
@staff_member_required
def toggle_product_status(request,product_id):
  if request.method=='POST':
    Product=get_object_or_404(product,id=product_id)
    Product.is_active= not Product.is_active
    Product.save()
  return redirect('product_list')

@never_cache
@staff_member_required
def add_product(request):
  if request.method=='POST':
    form=ProductForm(request.POST,request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request,"Product added succesfully, please add the variants")
      return redirect('add_variant')
  else:
    form=ProductForm()
  Categories=categories.objects.all()
  return render(request,'admin/admin_products_add.html',{'form':form ,'categories': Categories})

@never_cache
@staff_member_required
def edit_product(request,product_id):
  Product=get_object_or_404(product,id=product_id)

  if request.method=='POST':
    form=ProductForm(request.POST,request.FILES,instance=Product)
    if form.is_valid():
      form.save()
      return redirect('product_list')
  else:
    form=ProductForm(instance=Product)

  Categories=categories.objects.all()
  return render(request,'admin/admin_products_edit.html',
                {'form': form, 'categories': Categories, 'product': Product})  

@never_cache
def productDetails(request,product_id):
  Product = get_object_or_404(product, id=product_id)
    
    # Get the selected size from the request or default to 'M'
  selected_size = request.GET.get('size')

  print(f"the selected size is {selected_size}")
    
    # If no size is selected, find a default
  if not selected_size:
    # Prioritize 'M' size, fallback to first variant
    print("the selected size is null , if not is working")
    variant = (
        Product.variants.filter(size='M').first() or 
        Product.variants.first()
    )
  else:
    # Find variant by selected size
    variant = Product.variants.filter(size=selected_size).first()
  best_discount=Product.get_best_discount()
  discounted_price=Product.get_discounted_price()
    
  return render(request, 'user/product_details.html', {
        'product': Product,
        'variant': variant,
        'best_discount': best_discount,
        'discounted_price':discounted_price
    })

@never_cache
@staff_member_required
def variant_list(request,product_id):
  Product=get_object_or_404(product,id=product_id)
  variants=Product.variants.all()
  return render(request,'admin/variant_list.html',{'product': Product,'variants':variants})

@never_cache
@staff_member_required
def add_variant(request,product_id):
  product_instance = get_object_or_404(product, id=product_id)
  
  if request.method == 'POST':
    form = VariantForm(request.POST, product_instance=product_instance)
    if form.is_valid():
      variant = form.save(commit=False)
      variant.product = product_instance
      variant.save()
      return redirect('variant_list', product_id=product_id)
  else:
    form = VariantForm(product_instance=product_instance)
  
  return render(request, 'admin/add_variant.html', {
    'form': form,
    'product': product_instance
  })

@never_cache
@staff_member_required
def edit_variant(request,Variant_id):
  variant=get_object_or_404(Variant,id=Variant_id)
  if request.method=='POST':
    form=VariantForm(request.POST,instance=variant)
    if form.is_valid():
      form.save()
      return redirect('variant_list',product_id=variant.product.id)
  else:
    form=VariantForm(instance=variant)
  return render(request,'admin/edit_variant.html',{'form':form, 'variant': variant})

@never_cache
def all_products(request):
  
  products=product.objects.exclude(is_active=False)

  search_query=request.GET.get('search', '')
  if search_query:
    products=product.objects.filter(
      Q(name__icontains=search_query)| Q(description__icontains=search_query)
    ).exclude(is_active=False)


  min_price=request.GET.get('min_price','')
  max_price=request.GET.get('max_price','')
  if min_price:
    products=products.filter(price__gte=min_price).exclude(is_active=False)


  if max_price:
    products=products.filter(price__lte=max_price).exclude(is_active=False)


  sort_option=request.GET.get('sort', '')
  
  if sort_option=='price_asc':
    products=products.order_by('price').exclude(is_active=False)

  elif sort_option=='price_desc':
    products=products.order_by('-price').exclude(is_active=False)

  elif sort_option=='name_asc':
    products=products.order_by('name').exclude(is_active=False)

  elif sort_option=='name_desc':
    products=products.order_by('-name').exclude(is_active=False)

  category_id = request.GET.get('category', None)
  if category_id:
    products = products.filter(category_id=category_id)

  Categories=categories.objects.all()

  return render(request,'user/all_products.html',{'products': products, 'categories': Categories})
