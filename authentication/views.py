from django.shortcuts import render, redirect
from .forms import SignupForm, DepositForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import UserProfile
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                messages.success(request, 'New Account Created Successfully! You can login now.')
                form.save()
        else:
            form = SignupForm()
        return render(request, 'signup.html', {'form': form})
    else:
        return redirect('profile')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data = request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                userpass = form.cleaned_data['password']
                user = authenticate(username = name, password = userpass) 
                if user is not None:
                    login(request, user)
                    return redirect('homepage') 
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})
    else:
        return redirect('homepage')
    
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'authentication/profile.html')
