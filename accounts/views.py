from django.shortcuts import render

# Create your views here.
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# accounts/views.py
# Add these imports at the top
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
import random

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user type
                if user.user_type == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('distributor_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def admin_dashboard_view(request):
    # Simple protection: ensure only admins can see this
    if request.user.user_type != 'admin':
        return redirect('login') # or some other page
    return render(request, 'accounts/admin_dashboard.html')

@login_required
def distributor_dashboard_view(request):
    # Simple protection: ensure only distributors can see this
    if request.user.user_type != 'distributor':
        return redirect('login') # or some other page
    return render(request, 'accounts/distributor_dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')



# ... (keep the existing views)

def password_reset_request_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            # Generate a 6-digit OTP
            otp = random.randint(100000, 999999)
            # Store OTP and email in session
            request.session['reset_otp'] = otp
            request.session['reset_email'] = email

            # Send email
            subject = 'Your Password Reset OTP'
            message = f'Your OTP for password reset is: {otp}'
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, message, from_email, [email])

            return redirect('password_reset_otp')
        except CustomUser.DoesNotExist:
            # Handle case where email doesn't exist
            pass # You can add an error message here
    return render(request, 'accounts/password_reset_request.html')

def password_reset_otp_view(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_session = request.session.get('reset_otp')

        if int(otp_entered) == otp_session:
            email = request.session.get('reset_email')
            new_password = request.POST.get('new_password')
            user = CustomUser.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            # Clear session data
            del request.session['reset_otp']
            del request.session['reset_email']

            return redirect('login')
        else:
            # Handle incorrect OTP
            pass # You can add an error message here
    return render(request, 'accounts/password_reset_otp.html')