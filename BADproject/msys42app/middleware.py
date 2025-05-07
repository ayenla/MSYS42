from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from django.conf import settings
import re

class RoleMiddleware(MiddlewareMixin):
    """
    Middleware to enforce role-based permissions.
    - Admin: Access to all pages
    - Medical Staff: Access to all pages except user management
    - Program Coordinator: Access to view pages only
    """
    
    # URLs that don't require login
    PUBLIC_URLS = [
        r'^/login/$',
        r'^/logout/$',
        r'^/static/',
        r'^/media/',
    ]
    
    # URLs that only admins can access
    ADMIN_ONLY_URLS = [
        r'^/users/',
    ]
    
    # URLs that require write access (Medical Staff and Admin)
    WRITE_ACCESS_URLS = [
        # Child profiles
        r'^/CreateChildProfile/$',
        r'^/edit/\d+/$',
        r'^/edit-education/\d+/\d+/$',
        r'^/delete-education/\d+/\d+/$',
        
        # Medical history
        r'^/medical-history/add/\d+/$',
        
        # Physician's exam
        r'^/physician-exam/add/\d+/$',
        r'^/physician-exam/edit/\d+/\d+/$',
        r'^/physician-exam/delete/\d+/\d+/$',
        
        # Annual medical check
        r'^/child/\d+/annual-medical-check/create/$',
        r'^/child/\d+/annual-medical-check/\d+/edit/$',
        r'^/child/\d+/annual-medical-check/\d+/delete/$',
        
        # Family medical records
        r'^/family-medical-records/\d+/edit/\d+/$',
        r'^/family-medical-records/\d+/edit-family-information/\d+/$',
        r'^/family-medical-records/\d+/delete-family-member/\d+/$',
        r'^/family-medical-records/\d+/delete-family-medical-record/\d+/\d+/$'
    ]
    
    def process_request(self, request):
        # Skip middleware for non-authenticated paths
        path = request.path_info
        
        # Always allow access to login/logout pages
        if any(re.match(pattern, path) for pattern in self.PUBLIC_URLS):
            return None
            
        # Check if user is authenticated
        if not request.user.is_authenticated:
            if path != settings.LOGIN_URL:
                return redirect(settings.LOGIN_URL)
            return None
            
        # Check if user has a profile
        if not hasattr(request.user, 'profile'):
            if path not in ['/admin/', '/admin/login/'] and not path.startswith('/admin/'):
                messages.error(request, "Your account doesn't have a user profile. Please contact an administrator.")
                return redirect(settings.LOGIN_URL)
            return None
            
        # Admin can access everything
        if request.user.profile.is_admin():
            return None
            
        # Check admin-only URLs
        if any(re.match(pattern, path) for pattern in self.ADMIN_ONLY_URLS):
            messages.error(request, "You don't have permission to access this page.")
            return redirect('home')
            
        # Check write access URLs for Program Coordinators
        if request.user.profile.role == 'program_coordinator':
            if any(re.match(pattern, path) for pattern in self.WRITE_ACCESS_URLS) or request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
                messages.error(request, "Program Coordinators have view-only access.")
                # Extract the main part of the path (e.g., /child/123/...)
                main_path = '/'
                if path.startswith('/family-medical-records/'):
                    # Get child ID from the URL
                    match = re.match(r'^/family-medical-records/(\d+)/', path)
                    if match:
                        child_id = match.group(1)
                        main_path = f'/view/{child_id}/'
                elif path.startswith('/child/'):
                    # Get child ID from the URL 
                    match = re.match(r'^/child/(\d+)/', path)
                    if match:
                        child_id = match.group(1)
                        main_path = f'/view/{child_id}/'
                elif re.match(r'^/edit/\d+/$', path):
                    # Extract child ID from edit URL
                    match = re.match(r'^/edit/(\d+)/$', path)
                    if match:
                        child_id = match.group(1)
                        main_path = f'/view/{child_id}/'
                elif re.match(r'^/medical-history/add/\d+/$', path):
                    # Extract child ID from medical history URL
                    match = re.match(r'^/medical-history/add/(\d+)/$', path)
                    if match:
                        child_id = match.group(1)
                        main_path = f'/medical-history/view/{child_id}/'
                elif re.match(r'^/physician-exam/(add|edit|delete)/\d+/', path):
                    # Extract child ID from physician's exam URL
                    match = re.match(r'^/physician-exam/(add|edit|delete)/(\d+)/', path)
                    if match:
                        child_id = match.group(2)
                        main_path = f'/physician-exam/home/{child_id}/'
                
                # Redirect to main path or home if can't determine
                return redirect(main_path if main_path != '/' else 'home')
                
        return None 