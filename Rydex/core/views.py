from django.shortcuts import render
from categories.models import categories
from products.models import product
from django.views.decorators.cache import never_cache


# Create your views here.
@never_cache
def home(request):
  Categories = categories.objects.all()
  products = product.objects.select_related('category', 'offer').filter(
      is_active=True, variants__is_deleted=False
  ).distinct()[:8]
  new_arrivals = product.objects.select_related('category', 'offer').filter(
      is_active=True, variants__is_deleted=False
  ).distinct().order_by('-created_at')[:4]
  context = {
    'categories': Categories, 
    'products': products, 
    'new_arrivals': new_arrivals
  }
  return render(request, 'user/homepage.html', context)


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)


def custom_403(request, exception=None):
    return render(request, '403.html', status=403)


def custom_400(request, exception=None):
    return render(request, '400.html', status=400)