from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, Patient, Doctor, Prescription, MedicalRecord
from .forms import AppointmentForm, DoctorAppointmentForm
from .models import Appointment, Patient
from .forms import AppointmentForm
from clinic_app.models import MedicalRecord
from django.urls import reverse

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

# ...existing code...
def appointment_edit(request, id):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('clinic_app:home')
    appointment = get_object_or_404(Appointment, id=id, doctor=doctor)
    
    if request.method == "POST":
        form = DoctorAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            # use the URL kwarg name expected by the doctor_appointment_detail route
            return redirect('clinic_app:doctor_appointment_detail', appointment_id=appointment.id)
    else:
        form = DoctorAppointmentForm(instance=appointment)
    
    context = {
        'title': 'Edit Appointment',
        'form': form,
        'appointment': appointment,   # <-- add this so template can use appointment.id
        'object': appointment,        # <-- optional, keeps your current template's object variable
    }
    return render(request, 'clinic_app/appointment/edit.html', context)

def appointment_delete(request, id):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('clinic_app:home')
    appointment = get_object_or_404(Appointment, id=id, doctor=doctor)
    if request.method == "POST":
        appointment.delete()
        messages.success(request, 'Appointment has been deleted.')
        return redirect('clinic_app:doctor_dashboard')
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
    
    # Show only Pending and Approved appointments (exclude Completed)
    appointments = Appointment.objects.filter(
        doctor=doctor
    ).exclude(status='Completed').order_by('-appointment_date')
    
    # Get statistics (include all for stats)
    all_appointments = Appointment.objects.filter(doctor=doctor)
    pending_count = all_appointments.filter(status='Pending').count()
    approved_count = all_appointments.filter(status='Approved').count()
    completed_count = all_appointments.filter(status='Completed').count()
    total_count = all_appointments.count()
    
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
    
    # Get prescription if exists
    try:
        prescription = Prescription.objects.get(appointment=appointment)
    except Prescription.DoesNotExist:
        prescription = None
    
    context = {
        'title': 'Appointment Details',
        'appointment': appointment,
        'prescription': prescription,
        'doctor': doctor,
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
        
        # Create medical record if it doesn't exist
        if not hasattr(appointment, 'medical_record'):
            MedicalRecord.objects.create(
                appointment=appointment,
                subjective_notes='',
                objective_findings='',
                diagnosis='',
                treatment_plan='',
                follow_up_instructions=''
            )
        
        messages.success(request, 'Appointment has been marked as completed. Please add medical record details.')
    
    return redirect('clinic_app:doctor_appointment_detail', appointment_id=appointment_id)


@login_required(login_url='clinic_app:doctor_login')
def doctor_cancel_appointment(request, appointment_id):
    """Cancel an appointment"""
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('clinic_app:home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment has been cancelled.')
        return redirect('clinic_app:doctor_dashboard')
    
    return redirect('clinic_app:doctor_appointment_detail', appointment_id=appointment_id)


@login_required(login_url='clinic_app:doctor_login')
def doctor_add_prescription(request, appointment_id):
    """Add prescription to an appointment"""
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('clinic_app:home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    
    # Check if prescription already exists
    if hasattr(appointment, 'prescription'):
        messages.warning(request, 'A prescription already exists for this appointment.')
        return redirect('clinic_app:doctor_appointment_detail', appointment_id=appointment_id)
    
    if request.method == 'POST':
        medication = request.POST.get('medication')
        instructions = request.POST.get('instructions')
        
        if medication and instructions:
            Prescription.objects.create(
                appointment=appointment,
                medication=medication,
                instructions=instructions
            )
            messages.success(request, 'Prescription has been added successfully.')
            return redirect('clinic_app:doctor_appointment_detail', appointment_id=appointment_id)
        else:
            messages.error(request, 'Please fill in all fields.')
    
    context = {
        'title': 'Add Prescription',
        'appointment': appointment,
        'doctor': doctor,
    }
    return render(request, 'clinic_app/doctor/add_prescription.html', context)


@login_required(login_url='clinic_app:doctor_login')
def doctor_edit_prescription(request, prescription_id):
    """Edit an existing prescription"""
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('clinic_app:home')
    
    prescription = get_object_or_404(Prescription, id=prescription_id)
    
    # Verify the prescription belongs to this doctor's appointment
    if prescription.appointment.doctor != doctor:
        messages.error(request, 'You do not have permission to edit this prescription.')
        return redirect('clinic_app:doctor_dashboard')
    
    if request.method == 'POST':
        medication = request.POST.get('medication')
        instructions = request.POST.get('instructions')
        
        if medication and instructions:
            prescription.medication = medication
            prescription.instructions = instructions
            prescription.save()
            messages.success(request, 'Prescription has been updated successfully.')
            return redirect('clinic_app:doctor_appointment_detail', appointment_id=prescription.appointment.id)
        else:
            messages.error(request, 'Please fill in all fields.')
    
    context = {
        'title': 'Edit Prescription',
        'prescription': prescription,
        'appointment': prescription.appointment,
        'doctor': doctor,
    }
    return render(request, 'clinic_app/doctor/edit_prescription.html', context)


@login_required
def doctor_logout(request):
    """Doctor logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('clinic_app:doctor_login')


@login_required
def doctor_medical_records(request):
    # Ensure user is a doctor
    if not hasattr(request.user, 'doctor'):
        return redirect('clinic_app:doctor_dashboard')
    doctor = request.user.doctor
    q = request.GET.get('q', '').strip()
    
    # Get all completed appointments with medical records
    records = (MedicalRecord.objects
               .select_related('appointment__doctor__user')
               .filter(appointment__doctor=doctor, appointment__status='Completed')
               .order_by('-updated_at'))
    
    if q:
        records = records.filter(appointment__patient_name__icontains=q)
    
    return render(request, 'clinic_app/doctor/medical_records.html', {
        'page_title': 'Medical Records',
        'records': records,
        'query': q,
        'doctor': doctor
    })

@login_required(login_url='clinic_app:doctor_login')
def doctor_edit_medical_record(request, record_id):
    """Edit medical record"""
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('clinic_app:home')
    
    record = get_object_or_404(MedicalRecord, id=record_id, appointment__doctor=doctor)
    
    if request.method == 'POST':
        record.subjective_notes = request.POST.get('subjective_notes', '')
        record.objective_findings = request.POST.get('objective_findings', '')
        record.diagnosis = request.POST.get('diagnosis', '')
        record.treatment_plan = request.POST.get('treatment_plan', '')
        record.follow_up_instructions = request.POST.get('follow_up_instructions', '')
        record.save()
        
        messages.success(request, 'Medical record has been updated successfully.')
        return redirect('clinic_app:doctor_appointment_detail', appointment_id=record.appointment.id)
    
    context = {
        'title': 'Edit Medical Record',
        'record': record,
        'appointment': record.appointment,
        'doctor': doctor,
    }
    return render(request, 'clinic_app/doctor/edit_medical_record.html', context)