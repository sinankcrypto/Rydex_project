from django.shortcuts import render,redirect,get_object_or_404
from .models import categories
from django.contrib import messages
from .forms import categoryform
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from utils.pagination import paginate_queryset

# Create your views here.
@login_required
@never_cache
def category_list(request):
  active_categories=categories.objects.filter(is_listed=True)
  inactive_categories=categories.objects.filter(is_listed=False)

  active_categories = paginate_queryset(
      request,
      active_categories,
      per_page=4,
      page_param='page'
  )

  inactive_categories = paginate_queryset(
      request,
      inactive_categories,
      per_page=4,
      page_param='inactive_page'
  )
  
  return render(
      request,'admin/admin_categories.html',
      {
        'active_categories': active_categories,
        'inactive_categories': inactive_categories,
      }
    )

@never_cache
@staff_member_required
def add_category(request):
  if request.method=='POST':
    form=categoryform(request.POST,request.FILES)
    
    if form.is_valid():
      category= form.save(commit=False)
      uploaded_image = form.cleaned_data.get('image')

      if uploaded_image:
        try:
          image = Image.open(uploaded_image)
          width, height = image.size
          new_size = min(width, height)  # Square crop
          left = (width - new_size) / 2
          top = (height - new_size) / 2
          right = (width + new_size) / 2
          bottom = (height + new_size) / 2

          cropped_image = image.crop((left, top, right, bottom))
          buffer = BytesIO()
          img_format = image.format if image.format else 'JPEG'
          cropped_image.save(buffer, format=img_format)
          category.image.save(uploaded_image.name, ContentFile(buffer.getvalue()), save=False)
        except Exception:
          pass

      category.save()
      messages.success(request, "Category added successfully.")
      return redirect('category_list')
    else:
      return render(request,'admin/admin_categories_add.html',{'form': form}, status=400)
      
  else:
    form=categoryform()

  return render(request,'admin/admin_categories_add.html',{'form': form})

@staff_member_required
@never_cache
def edit_category(request,id):
  category=get_object_or_404(categories,id=id)

  if request.method=='POST':
    form=categoryform(request.POST,request.FILES,instance=category)

    if form.is_valid():
      cat = form.save(commit=False)
      uploaded_image = form.cleaned_data.get('image')
      if uploaded_image and 'image' in request.FILES:
        try:
          image = Image.open(uploaded_image)
          width, height = image.size
          new_size = min(width, height)
          left = (width - new_size) / 2
          top = (height - new_size) / 2
          right = (width + new_size) / 2
          bottom = (height + new_size) / 2

          cropped_image = image.crop((left, top, right, bottom))
          buffer = BytesIO()
          img_format = image.format if image.format else 'JPEG'
          cropped_image.save(buffer, format=img_format)
          cat.image.save(uploaded_image.name, ContentFile(buffer.getvalue()), save=False)
        except Exception:
          pass

      cat.save()
      messages.success(request, "Category updated successfully.")
      return redirect('category_list')
    else:
      return render(request,'admin/admin_categories_edit.html',{'form':form, 'category':category}, status=400)
  else:
    form=categoryform(instance=category)
  
  return render(request,'admin/admin_categories_edit.html',{'form':form, 'category':category})

@staff_member_required
def unlist_category(request,id):
  category=get_object_or_404(categories,id=id)
  category.is_listed=False
  category.save()
  return redirect('category_list')

@staff_member_required
def list_category(request,id):
  category=get_object_or_404(categories,id=id)
  category.is_listed=True
  category.save()
  return redirect('category_list')

@never_cache
def shop_by_category(request,category_id):
  category=get_object_or_404(categories,id=category_id)
  products=category.products.filter(is_active=True, variants__is_deleted=False).distinct()

  page_obj = paginate_queryset(
      request,
      products,
      per_page=8
  )

  return render(request,'user/shop_by_category.html',{'products': page_obj})