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
]

