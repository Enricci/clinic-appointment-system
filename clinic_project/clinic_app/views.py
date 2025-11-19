from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Appointment, Patient
from .forms import AppointmentForm

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

def patient_create_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = Patient.objects.get(user=request.user)
            appointment.save()
            return redirect('clinic_app:home')
    else:
        form = AppointmentForm()
    
    context = {
        'title': 'Create Appointment',
        'form': form
    }
    return render(request, 'clinic_app/patient/create_appointment.html', context)

def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'clinic_app/appointment/list.html', {'appointments': appointments})