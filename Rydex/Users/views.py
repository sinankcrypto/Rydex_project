from django.shortcuts import render,get_object_or_404,redirect
from user_auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages

# Create your views here.

@never_cache
@login_required(login_url='admin_login')
def Users_page(request):
  if not request.user.is_superuser:
    return render(request,'403.html',status=403)
  
  if request.method=='POST':
    user_id=request.POST.get('user_id')
    action=request.POST.get('action')
    if user_id and action:  # Ensure both values exist
      user = get_object_or_404(User, id=user_id)
      if action == 'block':
        user.is_active = False
        user.save()
        messages.success(request, f"{user.username} has been blocked.")
      elif action == 'unblock':
        user.is_active = True
        user.save()
        messages.success(request, f"{user.username} has been unblocked.")


    return redirect('users_page')

  users=User.objects.all()
  return render(request,'admin_users.html',{'users':users})


