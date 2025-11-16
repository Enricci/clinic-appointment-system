from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"
    
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    
class Appointment(models.Model):
    doctors = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patients = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    appointment_time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=50,
        choices = [
            ("Pending", "Pending"),
            ("Confirmed", "Confirmed"),
            ("Cancelled", "Cancelled"),
        ],
        default = "Pending",                      
    )
    
    def __str__(self):
        return f"Appointment with Dr. {self.doctors.user.last_name} for {self.patients.user.first_name} {self.patients.user.last_name} on {self.appointment_date.strftime('%Y-%m-%d')} at {self.appointment_time.strftime('%H:%M')}"
    

class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medication = models.CharField(max_length=255)
    instructions = models.TextField()
    
    def __str__(self):
        return f"Prescription for appointment on {self.appointment.appointment_date.strftime('%Y-%m-%d')} with Dr. {self.appointment.doctors.user.last_name}"