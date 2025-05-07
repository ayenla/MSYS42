from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required

def admin_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is an admin,
    redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and hasattr(u, 'profile') and u.profile.is_admin(),
        login_url='login',
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def medical_staff_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is a medical staff member,
    redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and hasattr(u, 'profile') and u.profile.is_medical_staff(),
        login_url='login',
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def role_required(allowed_roles=[]):
    """
    Decorator for views that checks that the user has one of the specified roles,
    redirecting to the login page if necessary.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if not hasattr(request.user, 'profile'):
                raise PermissionDenied("User profile not found")
                
            if request.user.profile.role in allowed_roles or request.user.profile.is_admin():
                return view_func(request, *args, **kwargs)
            
            # If user doesn't have permission, raise PermissionDenied
            raise PermissionDenied("You don't have permission to view this page")
        return wrapper
    return decorator 