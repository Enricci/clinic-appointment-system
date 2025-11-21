from django.urls import path
from . import views

app_name = 'clinic_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('patient/create-appointment/', views.patient_create_appointment, name='patient_create_appointment'),
    path('appointment/list/', views.appointment_list, name='appointment_list'),
    path('appointment/<int:id>/edit/', views.appointment_edit, name='appointment_edit'),
    path('appointment/<int:id>/delete/', views.appointment_delete, name='appointment_delete'),
    
    # Doctor URLs
    path('doctor/login/', views.doctor_login, name='doctor_login'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/logout/', views.doctor_logout, name='doctor_logout'),
    path('doctor/appointment/<int:appointment_id>/', views.doctor_appointment_detail, name='doctor_appointment_detail'),
    path('doctor/appointment/<int:appointment_id>/approve/', views.doctor_approve_appointment, name='doctor_approve_appointment'),
    path('doctor/appointment/<int:appointment_id>/complete/', views.doctor_complete_appointment, name='doctor_complete_appointment'),
    path('doctor/appointment/<int:appointment_id>/cancel/', views.doctor_cancel_appointment, name='doctor_cancel_appointment'),
    path('doctor/prescription/add/<int:appointment_id>/', views.doctor_add_prescription, name='doctor_add_prescription'),
    path('doctor/prescription/edit/<int:prescription_id>/', views.doctor_edit_prescription, name='doctor_edit_prescription'),
]

