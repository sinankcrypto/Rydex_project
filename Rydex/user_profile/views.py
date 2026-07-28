from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user_profile.forms import ProfilePictureForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from user_auth.models import User
from user_profile.models import profile
from django.views.decorators.cache import never_cache
from django.templatetags.static import static 
from utils.pagination import paginate_queryset
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from user_auth.views import send_otp_email, generate_otp
from django.conf import settings
from django.utils import timezone


@login_required
def add_profile_pic(request):
  if request.method=='POST':
    form=ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
    if form.is_valid():
      form.save()
      return redirect('profile')
  return redirect('profile')

@login_required
def edit_profile_pic(request):
  if request.method=='POST':
    form=ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
    if form.is_valid():
      form.save()
      return redirect('profile')
  return redirect('profile')

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs,):
  if created:
    profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
  instance.profile.save()

@login_required(login_url='login')
@never_cache
def wallet_view(request):
  user=request.user
  transactions=user.wallet_transactions.all().order_by('-created_at')

  transactions = paginate_queryset(
      request,
      transactions,
      per_page=5
  )

  profile_picture=user.profile.profile_picture.url if user.profile.profile_picture else static('images/profile_placeholder.png')
  return render(request,'user/wallet.html',{'user': user, 'transactions': transactions, 'profile_picture': profile_picture})


@login_required(login_url='login')
def change_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('username', '').strip()
        if not new_username:
            messages.error(request, "Username cannot be empty.")
            return redirect('profile')
        
        if new_username == request.user.username:
            messages.info(request, "Username is unchanged.")
            return redirect('profile')

        if User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
            messages.error(request, "Username is already taken. Please choose a different one.")
            return redirect('profile')

        request.user.username = new_username
        request.user.save()
        messages.success(request, "Username updated successfully!")
    return redirect('profile')


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('profile')

        if not new_password or len(new_password) < 6:
            messages.error(request, "New password must be at least 6 characters long.")
            return redirect('profile')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('profile')

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, "Password updated successfully!")
    return redirect('profile')


@login_required(login_url='login')
def change_email_request(request):
    if request.method == 'POST':
        new_email = request.POST.get('email', '').strip()

        try:
            validate_email(new_email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return redirect('profile')

        if new_email.lower() == request.user.email.lower():
            messages.info(request, "Email is unchanged.")
            return redirect('profile')

        if User.objects.filter(email__iexact=new_email).exclude(id=request.user.id).exists():
            messages.error(request, "This email address is already in use.")
            return redirect('profile')

        otp = generate_otp()
        request.session['email_change_new_email'] = new_email
        request.session['email_change_otp'] = otp
        request.session['email_change_otp_created_at'] = timezone.now().timestamp()

        send_otp_email(new_email, otp)

        messages.success(request, f"An OTP has been sent to {new_email}. Please enter it below to verify.")
        return redirect('verify_email_change_otp')

    return redirect('profile')


@login_required(login_url='login')
def verify_email_change_otp(request):
    new_email = request.session.get('email_change_new_email')
    session_otp = request.session.get('email_change_otp')
    otp_created_at = request.session.get('email_change_otp_created_at')

    expiry_minutes = getattr(settings, 'OTP_EXPIRY_MINUTES', 2)
    expiry_seconds = expiry_minutes * 60

    if not new_email or not session_otp or not otp_created_at:
        messages.error(request, "Session expired or no pending email change found.")
        return redirect('profile')

    current_time = timezone.now().timestamp()
    elapsed_time = current_time - otp_created_at
    is_expired = elapsed_time > expiry_seconds

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if is_expired:
            messages.error(request, "OTP has expired. Please request a new OTP.")
            return redirect('verify_email_change_otp')

        if entered_otp == session_otp:
            request.user.email = new_email
            request.user.save()

            request.session.pop('email_change_new_email', None)
            request.session.pop('email_change_otp', None)
            request.session.pop('email_change_otp_created_at', None)

            messages.success(request, "Email address updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    remaining_seconds = max(0, int(expiry_seconds - elapsed_time))

    context = {
        'new_email': new_email,
        'remaining_seconds': remaining_seconds,
        'is_expired': is_expired,
        'otp_expiry_minutes': expiry_minutes,
    }

    return render(request, 'user/verify_email_otp.html', context)


@login_required(login_url='login')
def resend_email_change_otp(request):
    if request.method == 'POST':
        new_email = request.session.get('email_change_new_email')
        if not new_email:
            messages.error(request, "Session expired. Please try changing your email again.")
            return redirect('profile')

        otp = generate_otp()
        request.session['email_change_otp'] = otp
        request.session['email_change_otp_created_at'] = timezone.now().timestamp()

        send_otp_email(new_email, otp)
        messages.success(request, f"A new OTP has been sent to {new_email}.")
        return redirect('verify_email_change_otp')

    return redirect('profile')