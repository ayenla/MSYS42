from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.models import User

from .forms import LoginForm, UserRegistrationForm, UserEditForm
from .models import UserProfile
from .decorators import admin_required, role_required

def login_view(request):
    """View for user login"""
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home page after login
    else:
        form = LoginForm()
    return render(request, 'msys42app/auth/login.html', {'form': form})

def logout_view(request):
    """View for user logout"""
    logout(request)
    return redirect('login')

@admin_required
def register_user(request):
    """View for user registration (admin only)"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            
            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role']
            )
            
            messages.success(request, 'User created successfully!')
            return redirect('user_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'msys42app/auth/register.html', {'form': form})

@admin_required
def user_list(request):
    """View for listing all users (admin only)"""
    users = User.objects.all().prefetch_related('profile')
    return render(request, 'msys42app/auth/user_list.html', {'users': users})

@admin_required
def user_edit(request, user_id):
    """View for editing user details (admin only)"""
    user = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user, defaults={'role': 'program_coordinator'})
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Update the profile separately
            profile.role = form.cleaned_data['role']
            profile.save()
            
            messages.success(request, 'User updated successfully!')
            return redirect('user_list')
    else:
        # Initialize form with both user and profile data
        initial_data = {
            'role': profile.role
        }
        form = UserEditForm(instance=user, initial=initial_data)
    return render(request, 'msys42app/auth/user_edit.html', {'form': form, 'user': user})

@admin_required
def user_delete(request, user_id):
    """View for deleting a user (admin only)"""
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('user_list')
    return render(request, 'msys42app/auth/user_delete_confirm.html', {'user': user}) 