from django.urls import path
from . import views

app_name = 'clinic_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('patient/create-appointment/', views.patient_create_appointment, name='patient_create_appointment'),
    
    # Doctor URLs
    path('doctor/login/', views.doctor_login, name='doctor_login'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/logout/', views.doctor_logout, name='doctor_logout'),
    path('doctor/appointment/<int:appointment_id>/', views.doctor_appointment_detail, name='doctor_appointment_detail'),
    path('doctor/appointment/<int:appointment_id>/approve/', views.doctor_approve_appointment, name='doctor_approve_appointment'),
    path('doctor/appointment/<int:appointment_id>/complete/', views.doctor_complete_appointment, name='doctor_complete_appointment'),
]

