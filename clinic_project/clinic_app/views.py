from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.

def home(request):
    """Home page view"""
    context = {
        'title': 'Home'
    }
    return render(request, 'clinic_app/home.html', context)


def register(request):
    """Registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome!')
            return redirect('clinic_app:home')
    else:
        form = UserCreationForm()
    
    context = {
        'title': 'Register',
        'form': form
    }
    return render(request, 'clinic_app/auth/registration.html', context)


def login_view(request):
    """Login view - redirect to Django's built-in login"""
    return redirect('/accounts/login/')


def logout_view(request):
    """Logout view - redirect to Django's built-in logout"""
    return redirect('/accounts/logout/')
