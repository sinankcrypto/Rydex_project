from django.shortcuts import render,redirect,get_object_or_404
from .models import CategoryOffer,ProductOffer
from .forms import CategoryOfferForm,ProductOfferForm
from django.contrib import messages
from django.core.exceptions import ValidationError

# Create your views here.

def offer_list(request):
  category_offers=CategoryOffer.objects.all()
  product_offers=ProductOffer.objects.all()
  return render(request,'admin/offers_list.html',{'category_offers': category_offers, 'product_offers': product_offers})

def add_category_offer(request):
  if request.method=='POST':
    form=CategoryOfferForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,'Category offer added successfully!')
      return redirect('offers_list')
  else:
    form=CategoryOfferForm()
  
  return render(request,'admin/add_category_offer.html',{'form': form})

def edit_category_offer(request,offer_id):
  offer=get_object_or_404(CategoryOffer,id=offer_id)
  if request.method=='POST':
    form=CategoryOfferForm(request.POST,instance=offer)
    if form.is_valid():
      form.save()
      messages.success(request,"category offer updated successfully!")
      return redirect('offers_list')
  else:
    form=CategoryOfferForm(instance=offer)
  return render(request,'admin/edit_category_offer.html',{'form': form, 'offer': offer, 'is_category_offer':True})

def delete_category_offer(request,offer_id):
  offer=get_object_or_404(CategoryOffer,id=offer_id)
  offer.delete()
  messages.success(request,'category offer deleted succesfully')
  return redirect('offers_list')

# product offers section

def add_product_offer(request):
  if request.method == 'POST':
    form = ProductOfferForm(request.POST)
     
    if form.is_valid():
      form.save()
      messages.success(request, "Product offer added successfully!")
      return redirect('offers_list')
    else:
      messages.error(request, "Please correct the errors below.")
  else:
    form = ProductOfferForm()
  return render(request, 'admin/add_product_offer.html', {'form': form})

def edit_product_offer(request,offer_id):
  offer=get_object_or_404(ProductOffer,id=offer_id)
  if request.method=='POST':
    form=ProductOfferForm(request.POST, instance=offer)
    if form.is_valid():
      form.save()
      messages.success(request, "Product offer updated successfully!")
      return redirect('offers_list')
  else:
    form=ProductOfferForm(instance=offer)
  return render(request,'admin/edit_product_offer.html',{'form': form,'offer':offer,'is_category_offer':False})

def delete_product_offer(request,offer_id):
  offer=get_object_or_404(ProductOffer,id=offer_id)
  offer.delete()
  messages.success(request,'product offer deleted succesfully')
  return redirect('offers_list')


