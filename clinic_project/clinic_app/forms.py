from datetime import datetime
from django import forms
from django.utils import timezone
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    # Additional patient information fields
    patient_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter patient full name"})
    )
    patient_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter patient email"})
    )
    patient_contact = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter contact number"})
    )
    
    class Meta:
        model = Appointment
        fields = ["doctor","patient_name", "patient_email", "patient_contact", "appointment_date", "appointment_time", "reason"]
        
        widgets = {
            "doctor": forms.Select(attrs={"class": "form-control"}),
            "patient_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter patient full name"}),
            "patient_email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter patient email"}),
            "patient_contact": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter contact number"}),
            "appointment_date": forms.HiddenInput(),
            "appointment_time": forms.HiddenInput(),
            "reason": forms.Textarea(attrs={"rows": 3, "placeholder": "Reason for appointment", "class": "form-control"}) 
        }
        
        labels = {
            "class": "form-label",
            "doctor": "Doctor",
            "patient_name": "Patient Name",
            "patient_email": "Patient Email",
            "patient_contact": "Patient Phone",
            "appointment_date": "Appointment Date",
            "appointment_time": "Appointment Time",
            "reason": "Reason for Appointment"
        }

class DoctorAppointmentForm(forms.ModelForm):
    def clean_appointment_date(self):
        appointment_date = self.cleaned_data.get('appointment_date')
        if appointment_date is None:
            raise forms.ValidationError("Appointment date is required.")
        if isinstance(appointment_date, datetime):
            appointment_date = appointment_date.date()
        today = timezone.localdate()
        if appointment_date < today:
            raise forms.ValidationError("The appointment date cannot be in the past.")
        return appointment_date

    def clean_appointment_time(self):
        date = self.cleaned_data.get('appointment_date')
        time = self.cleaned_data.get('appointment_time')
        
        if time is None:
            raise forms.ValidationError("Appointment time is required.")
        if date is None:
            return time
        
        if isinstance(date, datetime):
            date = date.date()
        
        if date == timezone.localdate():
            now_time = timezone.localtime().time()
            if time < now_time:
                raise forms.ValidationError("The appointment time cannot be in the past.")
        return time
    
    def clean_status(self):
        status = self.cleaned_data.get('status')
        date = self.cleaned_data.get('appointment_date')
        time = self.cleaned_data.get('appointment_time')
        if status == "Completed":
            if not date or not time:
                raise forms.ValidationError("Completed appointments must have a date and time.")
            appointment_datetime = timezone.make_aware(datetime.combine(date, time))
            if appointment_datetime > timezone.now():
                raise forms.ValidationError("Completed appointments cannot be set in the future.")
        if status == "Approved":
            if not date or not time:
                raise forms.ValidationError("Approved appointments must have a date and time.")
        return status

    class Meta:
        model = Appointment
        fields = ["doctor","patient_name", "patient_email", "patient_contact", "appointment_date", "appointment_time", "reason", "status"]
        
        widgets = {
            "doctor": forms.Select(attrs={"class": "form-control"}),
            "patient_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter patient full name"}),
            "patient_email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter patient email"}),
            "patient_contact": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter contact number"}),
            "appointment_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "appointment_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "reason": forms.Textarea(attrs={"rows": 3, "placeholder": "Reason for appointment", "class": "form-control"}) 
        }
        
        labels = {
            "doctor": "Doctor",
            "patient_name": "Patient Name",
            "patient_email": "Patient Email",
            "patient_contact": "Patient Phone",
            "appointment_date": "Appointment Date",
            "appointment_time": "Appointment Time",
            "status": "Status",
            "reason": "Reason for Appointment"
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['appointment_date'].required = True
        self.fields['appointment_time'].required = True