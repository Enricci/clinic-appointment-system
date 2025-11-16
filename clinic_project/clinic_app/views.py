from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    """Home page view"""
    context = {
        'title': 'Home',
        'page_title': 'Welcome to Clinic Appointment System'
    }
    return render(request, 'clinic_app/home.html', context)
