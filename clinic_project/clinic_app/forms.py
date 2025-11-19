from django import forms
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
        fields = ["doctor", "appointment_date", "appointment_time", "reason"]
        
        widgets = {
            "doctor": forms.Select(attrs={"class": "form-control"}),
            "appointment_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "appointment_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "reason": forms.Textarea(attrs={"rows": 3, "placeholder": "Reason for appointment", "class": "form-control"}) 
        }
        
        labels = {
            "class": "form-label",
            "doctor": "Doctor",
            "appointment_date": "Appointment Date",
            "appointment_time": "Appointment Time",
            "reason": "Reason for Appointment"
        }