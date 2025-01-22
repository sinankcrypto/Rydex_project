from django.shortcuts import render,redirect,get_object_or_404
from .models import categories
from django.contrib import messages
from .forms import categoryform
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
@never_cache
def category_list(request):
  active_categories=categories.objects.filter(is_listed=True)
  inactive_categories=categories.objects.filter(is_listed=False)

  return render(request,'admin/admin_categories.html',{
    'active_categories':active_categories, 
    'inactive_categories': inactive_categories})

def add_category(request):
  if request.method=='POST':
    form=categoryform(request.POST,request.FILES)
    
    if form.is_valid:
      category= form.save(commit=False)

      uploaded_image = form.cleaned_data['image']

      image = Image.open(uploaded_image)

      # Crop the image (center crop as an example)
      width, height = image.size
      new_size = min(width, height)  # Square crop
      left = (width - new_size) / 2
      top = (height - new_size) / 2
      right = (width + new_size) / 2
      bottom = (height + new_size) / 2

      cropped_image = image.crop((left, top, right, bottom))

      # Optional: Resize the cropped image
      #cropped_image = cropped_image.resize((300, 300))  # Resize to 300x300

      # Save the processed image back to the instance
      buffer = BytesIO()
      cropped_image.save(buffer, format=image.format)
      category.image.save(uploaded_image.name, ContentFile(buffer.getvalue()), save=False)

      category.save()
      return redirect('category_list')
      
  else:
    form=categoryform()

  return render(request,'admin/admin_categories_add.html',{'form': form})

def edit_category(request,id):
  category=get_object_or_404(categories,id=id)

  if request.method=='POST':
    form=categoryform(request.POST,request.FILES,instance=category)

    if form.is_valid():
      form.save()
      return redirect('category_list')
  else:
    form=categoryform(instance=category)
  
  return render(request,'admin/admin_categories_edit.html',{'form':form, 'category':category})

def unlist_category(request,id):
  category=get_object_or_404(categories,id=id)
  category.is_listed=False
  category.save()
  return redirect('category_list')

def list_category(request,id):
  category=get_object_or_404(categories,id=id)
  category.is_listed=True
  category.save()
  return redirect('category_list')

def shop_by_category(request,category_id):
  category=get_object_or_404(categories,id=category_id)
  products=category.products.exclude(is_active=False)

  return render(request,'user/shop_by_category.html',{'products': products})