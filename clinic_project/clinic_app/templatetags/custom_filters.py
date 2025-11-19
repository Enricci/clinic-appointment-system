from django import template
from clinic_app.models import Doctor

register = template.Library()


@register.filter(name='is_doctor')
def is_doctor(user):
    """Check if the user is a doctor"""
    if not user.is_authenticated:
        return False
    try:
        Doctor.objects.get(user=user)
        return True
    except Doctor.DoesNotExist:
        return False

