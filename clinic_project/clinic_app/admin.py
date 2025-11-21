from django.contrib import admin
from .models import Doctor, Patient, Appointment, Prescription


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'phone_number')
    search_fields = ('user__first_name', 'user__last_name', 'specialization')
    list_filter = ('specialization',)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'email', 'phone_number')
    search_fields = ('user__first_name', 'user__last_name', 'email', 'phone_number')
    list_filter = ('date_of_birth',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'patient_email', 'patient_contact', 'doctor', 'appointment_date', 'appointment_time', 'status')
    search_fields = ('patient_name', 'patient_email', 'doctor__user__last_name')
    list_filter = ('status', 'appointment_date', 'doctor__specialization')
    date_hierarchy = 'appointment_date'
    ordering = ('-appointment_date',)


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'medication', 'get_patient', 'get_doctor')
    search_fields = ('medication', 'appointment__patient__user__first_name', 'appointment__patient__user__last_name')
    
    def get_patient(self, obj):
        return obj.appointment.patient
    get_patient.short_description = 'Patient'
    
    def get_doctor(self, obj):
        return obj.appointment.doctor
    get_doctor.short_description = 'Doctor'
