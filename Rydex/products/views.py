from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from .models import product,Variant
from .forms import ProductForm,VariantForm
from categories.models import categories
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from utils.pagination import paginate_queryset

# Create your views here.

@never_cache
@staff_member_required
def product_list(request):
  products=product.objects.select_related('category', 'offer').all()

  page_obj = paginate_queryset(
        request,
        products,
        per_page=8
    )

  return render(request,'admin/admin_products.html',{"page_obj": page_obj,})

@never_cache
@staff_member_required
def toggle_product_status(request,product_id):
  if request.method=='POST':
    Product=get_object_or_404(product,id=product_id)
    if not Product.is_active:
      if not Product.variants.filter(is_deleted=False).exists():
        messages.error(request, "Cannot activate a product with no variants.")
        return redirect('product_list')
      Product.is_active = True
    else:
      Product.is_active = False
    Product.save()
  return redirect('product_list')

@never_cache
@staff_member_required
def add_product(request):
  if request.method=='POST':
    form=ProductForm(request.POST,request.FILES)
    if form.is_valid():
      prod=form.save(commit=False)
      prod.is_active = False
      prod.save()
      messages.success(request,"Product added successfully, please add the variants.")
      return redirect('add_variant',product_id=prod.id)
    else:
      Categories=categories.objects.all()
      return render(request,'admin/admin_products_add.html',{'form':form ,'categories': Categories}, status=400)
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
      prod = form.save(commit=False)
      if prod.is_active and not prod.variants.filter(is_deleted=False).exists():
        prod.is_active = False
        messages.warning(request, "Product cannot be active without variants.")
      prod.save()
      return redirect('product_list')
    else:
      Categories=categories.objects.all()
      return render(request,'admin/admin_products_edit.html',
                    {'form': form, 'categories': Categories, 'product': Product}, status=400)
  else:
    form=ProductForm(instance=Product)

  Categories=categories.objects.all()
  return render(request,'admin/admin_products_edit.html',
                {'form': form, 'categories': Categories, 'product': Product})  

@never_cache
def productDetails(request,product_id):
  Product = get_object_or_404(product, id=product_id, is_active=True)
  active_variants = Product.variants.filter(is_deleted=False)
  if not active_variants.exists():
    raise Http404("Product not available.")
    
  selected_size = request.GET.get('size')

  if not selected_size:
    variant = (
        active_variants.filter(size='M').first() or 
        active_variants.first()
    )
  else:
    variant = active_variants.filter(size=selected_size).first() or active_variants.first()
    
  best_discount=Product.get_best_discount()
  discounted_price=Product.get_discounted_price()
    
  return render(request, 'user/product_details.html', {
        'product': Product,
        'variant': variant,
        'variants': active_variants,
        'best_discount': best_discount,
        'discounted_price':discounted_price
    })

@never_cache
@staff_member_required
def variant_list(request,product_id):
  Product=get_object_or_404(product,id=product_id)
  variants=Product.variants.filter(is_deleted=False)

  page_obj = paginate_queryset(
      request,
      variants,
      per_page=10
  )
  return render(request,'admin/variant_list.html',{'product': Product,'page_obj':page_obj})

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
      return render(request, 'admin/add_variant.html', {
        'form': form,
        'product': product_instance
      }, status=400)
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
      return render(request,'admin/edit_variant.html',{'form':form, 'variant': variant}, status=400)
  else:
    form=VariantForm(instance=variant)
  return render(request,'admin/edit_variant.html',{'form':form, 'variant': variant})

@never_cache
@staff_member_required
def delete_variant(request, variant_id):
  variant = get_object_or_404(Variant, id=variant_id)

  if request.method == 'POST':
    parent_product = variant.product
    variant.is_deleted = True
    variant.save(update_fields=['is_deleted'])

    if not parent_product.variants.filter(is_deleted=False).exists():
      parent_product.is_active = False
      parent_product.save(update_fields=['is_active'])
      messages.warning(request, f"All variants deleted for '{parent_product.name}'. Product deactivated.")

    return redirect('variant_list', product_id=parent_product.id)

  return redirect('variant_list', product_id=variant.product.id)

@never_cache
def all_products(request):
  products = product.objects.filter(is_active=True, variants__is_deleted=False).distinct()

  search_query = request.GET.get('search', '').strip()
  if search_query:
    products = products.filter(
      Q(name__icontains=search_query) | Q(description__icontains=search_query)
    )

  min_price = request.GET.get('min_price', '').strip()
  max_price = request.GET.get('max_price', '').strip()
  if min_price:
    products = products.filter(price__gte=min_price)

  if max_price:
    products = products.filter(price__lte=max_price)

  category_id = request.GET.get('category', None)
  if category_id:
    products = products.filter(category_id=category_id)

  sort_option = request.GET.get('sort', '')
  if sort_option == 'price_asc':
    products = products.order_by('price')
  elif sort_option == 'price_desc':
    products = products.order_by('-price')
  elif sort_option == 'name_asc':
    products = products.order_by('name')
  elif sort_option == 'name_desc':
    products = products.order_by('-name')
  else:
    products = products.order_by('-created_at')

  page_obj = paginate_queryset(
        request,
        products,
        per_page=8
    )

  Categories = categories.objects.all()

  return render(request, 'user/all_products.html', {'products': page_obj, 'categories': Categories})
