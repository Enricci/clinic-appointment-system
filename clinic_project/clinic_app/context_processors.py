from .models import Doctor


def user_type(request):
    """Add user type information to all templates"""
    is_doctor = False
    if request.user.is_authenticated:
        try:
            Doctor.objects.get(user=request.user)
            is_doctor = True
        except Doctor.DoesNotExist:
            is_doctor = False
    
    return {
        'is_doctor': is_doctor
    }

