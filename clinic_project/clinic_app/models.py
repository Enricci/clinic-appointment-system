from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    
    def __str__(self):
        return f"Dr. {self.user.last_name}"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    
    def __str__(self):
        return self.user.get_full_name()
    
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100, default="Unknown")
    patient_email = models.EmailField(max_length=254, blank=True, null=True)
    patient_contact = models.CharField(max_length=20)
    appointment_date = models.DateTimeField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Approved", "Approved"),
            ("Completed", "Completed"),
        ],
        default="Pending"
    )
    
    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.last_name} for {self.patient_name} on {self.appointment_date}"
    
class MedicalRecord(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="medical_record")
    subjective_notes = models.TextField(help_text="Patient-reported symptoms, history", blank=True)
    objective_findings = models.TextField(help_text="Vitals, physical exam findings", blank=True)
    diagnosis = models.CharField(max_length=255, blank=True)
    treatment_plan = models.TextField(help_text="Therapies, interventions decided", blank=True)
    follow_up_instructions = models.TextField(help_text="Monitoring, next visit guidance", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Medical Record for {self.appointment.patient_name} ({self.appointment.id})"

class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    medication = models.TextField()
    instructions = models.TextField()
    
    def __str__(self):
        return f"Prescription for {self.appointment.patient_name}"