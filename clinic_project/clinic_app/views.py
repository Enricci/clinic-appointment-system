from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, Patient
from .forms import AppointmentForm, DoctorAppointmentForm
from .models import Appointment, Patient, Doctor
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
            appointment.appointment_date = None
            appointment.appointment_time = None
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

def appointment_edit(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    
    if request.method == "POST":
        form = DoctorAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('clinic_app:appointment_list')
    else:
        form = DoctorAppointmentForm(instance=appointment)
    
    context = {
        'title': 'Edit Appointment',
        'form': form
    }
    return render(request, 'clinic_app/appointment/edit.html', context)

def appointment_delete(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == "POST":
        appointment.delete()
        return redirect('clinic_app:appointment_list')
    return render(request, 'clinic_app/appointment/delete.html', {'appointment': appointment})


# Doctor Views
def doctor_login(request):
    """Doctor login view"""
    if request.user.is_authenticated:
        try:
            doctor = Doctor.objects.get(user=request.user)
            return redirect('clinic_app:doctor_dashboard')
        except Doctor.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    doctor = Doctor.objects.get(user=user)
                    login(request, user)
                    messages.success(request, f'Welcome, Dr. {user.last_name}!')
                    return redirect('clinic_app:doctor_dashboard')
                except Doctor.DoesNotExist:
                    messages.error(request, 'This account is not registered as a doctor.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    context = {
        'title': 'Doctor Login',
        'form': form
    }
    return render(request, 'clinic_app/auth/login.html', context)


@login_required(login_url='clinic_app:doctor_login')
def doctor_dashboard(request):
    """Doctor dashboard view"""
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('clinic_app:home')
    
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date')
    
    # Get statistics
    pending_count = appointments.filter(status='Pending').count()
    approved_count = appointments.filter(status='Approved').count()
    completed_count = appointments.filter(status='Completed').count()
    total_count = appointments.count()
    
    context = {
        'title': 'Doctor Dashboard',
        'doctor': doctor,
        'appointments': appointments,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'completed_count': completed_count,
        'total_count': total_count,
    }
    return render(request, 'clinic_app/doctor/dashboard.html', context)


@login_required(login_url='clinic_app:doctor_login')
def doctor_appointment_detail(request, appointment_id):
    """Doctor appointment detail view"""
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('clinic_app:home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    
    context = {
        'title': 'Appointment Details',
        'appointment': appointment,
    }
    return render(request, 'clinic_app/doctor/appointment_detail.html', context)


@login_required(login_url='clinic_app:doctor_login')
def doctor_approve_appointment(request, appointment_id):
    """Approve an appointment"""
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('clinic_app:home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    
    if request.method == 'POST':
        appointment.status = 'Approved'
        appointment.save()
        messages.success(request, 'Appointment has been approved.')
    
    return redirect('clinic_app:doctor_dashboard')


@login_required(login_url='clinic_app:doctor_login')
def doctor_complete_appointment(request, appointment_id):
    """Mark an appointment as completed"""
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('clinic_app:home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    
    if request.method == 'POST':
        appointment.status = 'Completed'
        appointment.save()
        messages.success(request, 'Appointment has been marked as completed.')
    
    return redirect('clinic_app:doctor_dashboard')


@login_required
def doctor_logout(request):
    """Doctor logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('clinic_app:doctor_login')