from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
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