from django.contrib import admin
from django.urls import path
from . import views
from . import views_auth

urlpatterns = [
    path('', views.home, name='home'),
    path('CreateChildProfile/', views.create_child_profile, name='create_child_profile'),
    path('view/<int:pk>/', views.view_child_profile, name='view_child_profile'),
    path('edit/<int:pk>/', views.edit_child_profile, name='edit_child_profile'),
    path('edit-education/<int:pk>/<int:id>/', views.edit_education, name='edit_education'),
    path('delete-education/<int:pk>/<int:id>/', views.delete_education, name='delete_education'),


    #Family Medical Records
    path('family-medical-records/<int:pk>/', views.view_family_medicals, name='view_family_medicals'),
    path('family-medical-records/<int:pk>/view/<int:id>/', views.view_family_medical_record, name='view_family_medical_record'),
    path('family-medical-records/<int:pk>/edit/<int:id>/', views.edit_family_medical_record, name='edit_family_medical_record'),
    path('family-medical-records/<int:pk>/edit-family-information/<int:id>/', views.edit_family_info, name='edit_family_info'),
    path('family-medical-records/<int:pk>/delete-family-member/<int:id>/', views.delete_family_member, name='delete_family_member'),
    path('family-medical-records/<int:pk>/delete-family-medical-record/<int:id>/<int:rec>/', views.delete_family_medical_record, name='delete_family_medical_record'),

    # Medical History Paths
    path('medical-history/add/<int:child_id>/', views.add_medical_history, name='create_medical_history'),
    path('medical-history/view/<int:child_id>/', views.view_medical_history, name='view_medical_history'), 

    #Physician's Exam
    path('physician-exam/home/<int:pk>/', views.home_physicians_exam, name='home_physicians_exam'),
    path('physician-exam/add/<int:pk>/', views.create_physicians_exam, name='create_physicians_exam'),
    path('physician-exam/view/<int:pk>/<int:id>/', views.view_physicians_exam, name='view_physicians_exam'),
    path('physician-exam/edit/<int:pk>/<int:id>/', views.edit_physicians_exam, name='edit_physicians_exam'),
    path('physician-exam/delete/<int:pk>/<int:id>/', views.delete_physicians_exam, name='delete_physicians_exam'),

    #Annual Medical Check
    path('child/<int:child_id>/annual-medical-check/', views.annual_medical_check_list, name='annual_medical_check_list'),
    path('child/<int:child_id>/annual-medical-check/create/', views.create_annual_medical_check, name='create_annual_medical_check'),
    path('child/<int:child_id>/annual-medical-check/<int:year>/', views.view_annual_medical_check, name='view_annual_medical_check'),
    path('child/<int:child_id>/annual-medical-check/<int:check_id>/edit/', views.edit_annual_medical_check, name='edit_annual_medical_check'),
    path('child/<int:child_id>/annual-medical-check/<int:check_id>/delete/', views.delete_annual_medical_check, name='delete_annual_medical_check'),

    # Authentication and user management URLs
    path('login/', views_auth.login_view, name='login'),
    path('logout/', views_auth.logout_view, name='logout'),
    path('users/', views_auth.user_list, name='user_list'),
    path('users/add/', views_auth.register_user, name='register_user'),
    path('users/<int:user_id>/edit/', views_auth.user_edit, name='user_edit'),
    path('users/<int:user_id>/delete/', views_auth.user_delete, name='user_delete'),
]
