from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from clinic_app.models import Doctor, Patient, Appointment, Prescription
from datetime import timedelta, date, time
import random


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Prescription.objects.all().delete()
        Appointment.objects.all().delete()
        Patient.objects.all().delete()
        Doctor.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # Create Doctors
        self.stdout.write('Creating doctors...')
        doctors_data = [
            {
                'username': 'dr_smith',
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'john.smith@clinic.com',
                'specialization': 'Cardiology',
                'phone': '+1-555-0101'
            },
            {
                'username': 'dr_johnson',
                'first_name': 'Emily',
                'last_name': 'Johnson',
                'email': 'emily.johnson@clinic.com',
                'specialization': 'Pediatrics',
                'phone': '+1-555-0102'
            },
            {
                'username': 'dr_williams',
                'first_name': 'Michael',
                'last_name': 'Williams',
                'email': 'michael.williams@clinic.com',
                'specialization': 'Orthopedics',
                'phone': '+1-555-0103'
            },
            {
                'username': 'dr_brown',
                'first_name': 'Sarah',
                'last_name': 'Brown',
                'email': 'sarah.brown@clinic.com',
                'specialization': 'Dermatology',
                'phone': '+1-555-0104'
            },
            {
                'username': 'dr_davis',
                'first_name': 'Robert',
                'last_name': 'Davis',
                'email': 'robert.davis@clinic.com',
                'specialization': 'Neurology',
                'phone': '+1-555-0105'
            },
            {
                'username': 'dr_martinez',
                'first_name': 'Maria',
                'last_name': 'Martinez',
                'email': 'maria.martinez@clinic.com',
                'specialization': 'Ophthalmology',
                'phone': '+1-555-0106'
            },
        ]
        
        doctors = []
        for doctor_data in doctors_data:
            user = User.objects.create_user(
                username=doctor_data['username'],
                first_name=doctor_data['first_name'],
                last_name=doctor_data['last_name'],
                email=doctor_data['email'],
                password='password123'
            )
            doctor = Doctor.objects.create(
                user=user,
                specialization=doctor_data['specialization'],
                phone_number=doctor_data['phone']
            )
            doctors.append(doctor)
            self.stdout.write(self.style.SUCCESS(f'  Created: Dr. {doctor_data["last_name"]} - {doctor_data["specialization"]}'))
        
        # Create Patients
        self.stdout.write('Creating patients...')
        patients_data = [
            {
                'username': 'alice_cooper',
                'first_name': 'Alice',
                'last_name': 'Cooper',
                'email': 'alice.cooper@email.com',
                'dob': date(1985, 3, 15),
                'phone': '+1-555-1001'
            },
            {
                'username': 'bob_taylor',
                'first_name': 'Bob',
                'last_name': 'Taylor',
                'email': 'bob.taylor@email.com',
                'dob': date(1990, 7, 22),
                'phone': '+1-555-1002'
            },
            {
                'username': 'charlie_wilson',
                'first_name': 'Charlie',
                'last_name': 'Wilson',
                'email': 'charlie.wilson@email.com',
                'dob': date(1978, 11, 8),
                'phone': '+1-555-1003'
            },
            {
                'username': 'diana_moore',
                'first_name': 'Diana',
                'last_name': 'Moore',
                'email': 'diana.moore@email.com',
                'dob': date(1992, 5, 30),
                'phone': '+1-555-1004'
            },
            {
                'username': 'edward_jackson',
                'first_name': 'Edward',
                'last_name': 'Jackson',
                'email': 'edward.jackson@email.com',
                'dob': date(1988, 9, 12),
                'phone': '+1-555-1005'
            },
            {
                'username': 'fiona_white',
                'first_name': 'Fiona',
                'last_name': 'White',
                'email': 'fiona.white@email.com',
                'dob': date(1995, 2, 18),
                'phone': '+1-555-1006'
            },
            {
                'username': 'george_harris',
                'first_name': 'George',
                'last_name': 'Harris',
                'email': 'george.harris@email.com',
                'dob': date(1982, 6, 25),
                'phone': '+1-555-1007'
            },
            {
                'username': 'hannah_martin',
                'first_name': 'Hannah',
                'last_name': 'Martin',
                'email': 'hannah.martin@email.com',
                'dob': date(1987, 12, 5),
                'phone': '+1-555-1008'
            },
        ]
        
        patients = []
        for patient_data in patients_data:
            user = User.objects.create_user(
                username=patient_data['username'],
                first_name=patient_data['first_name'],
                last_name=patient_data['last_name'],
                email=patient_data['email'],
                password='password123'
            )
            patient = Patient.objects.create(
                user=user,
                date_of_birth=patient_data['dob'],
                email=patient_data['email'],
                phone_number=patient_data['phone']
            )
            patients.append(patient)
            self.stdout.write(self.style.SUCCESS(f'  Created: {patient_data["first_name"]} {patient_data["last_name"]}'))
        
        # Create Appointments
        self.stdout.write('Creating appointments...')
        appointment_reasons = [
            'Annual checkup',
            'Follow-up consultation',
            'Severe headache and dizziness',
            'Chest pain and discomfort',
            'Skin rash treatment',
            'Vision problems',
            'Back pain assessment',
            'Regular health screening',
            'Difficulty sleeping',
            'Joint pain evaluation',
            'Respiratory issues',
            'Routine examination',
        ]
        
        statuses = ['Pending', 'Approved', 'Completed']
        appointments = []
        
        # Create appointments for the next 30 days
        for i in range(15):
            appointment_date = timezone.now() + timedelta(days=random.randint(0, 30))
            appointment_time = time(hour=random.randint(9, 16), minute=random.choice([0, 15, 30, 45]))
            
            appointment = Appointment.objects.create(
                doctor=random.choice(doctors),
                patient=random.choice(patients),
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                reason=random.choice(appointment_reasons),
                status=random.choice(statuses)
            )
            appointments.append(appointment)
            self.stdout.write(self.style.SUCCESS(
                f'  Created: Appointment #{i+1} - {appointment.patient} with Dr. {appointment.doctor.user.last_name}'
            ))
        
        # Create Prescriptions for completed appointments
        self.stdout.write('Creating prescriptions...')
        completed_appointments = [apt for apt in appointments if apt.status == 'Completed']
        
        prescriptions_data = [
            {
                'medication': 'Amoxicillin 500mg',
                'instructions': 'Take one capsule three times daily for 7 days. Complete the full course even if symptoms improve.'
            },
            {
                'medication': 'Ibuprofen 400mg',
                'instructions': 'Take one tablet every 6-8 hours as needed for pain. Do not exceed 4 tablets in 24 hours. Take with food.'
            },
            {
                'medication': 'Lisinopril 10mg',
                'instructions': 'Take one tablet once daily in the morning. Monitor blood pressure regularly.'
            },
            {
                'medication': 'Metformin 500mg',
                'instructions': 'Take one tablet twice daily with meals. Monitor blood sugar levels regularly.'
            },
            {
                'medication': 'Omeprazole 20mg',
                'instructions': 'Take one capsule once daily before breakfast for 14 days.'
            },
            {
                'medication': 'Hydrocortisone Cream 1%',
                'instructions': 'Apply thin layer to affected area twice daily for up to 7 days. Wash hands after application.'
            },
        ]
        
        for appointment in completed_appointments[:min(6, len(completed_appointments))]:
            prescription_data = random.choice(prescriptions_data)
            prescription = Prescription.objects.create(
                appointment=appointment,
                medication=prescription_data['medication'],
                instructions=prescription_data['instructions']
            )
            self.stdout.write(self.style.SUCCESS(
                f'  Created: Prescription for {appointment.patient}'
            ))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'Doctors created: {Doctor.objects.count()}')
        self.stdout.write(f'Patients created: {Patient.objects.count()}')
        self.stdout.write(f'Appointments created: {Appointment.objects.count()}')
        self.stdout.write(f'Prescriptions created: {Prescription.objects.count()}')
        self.stdout.write('\nDefault password for all users: password123')
        self.stdout.write(self.style.SUCCESS('='*50))

