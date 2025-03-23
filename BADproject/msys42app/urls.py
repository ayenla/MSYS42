
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('CreateChildProfile/', views.create_child_profile, name='create_child_profile'),
    path('view/<int:pk>/', views.view_child_profile, name='view_child_profile'),
    path('edit/<int:pk>/', views.edit_child_profile, name='edit_child_profile'),

    # Medical History Paths
    path('medical-history/add/<int:child_id>/', views.add_medical_history, name='create_medical_history'),
    path('medical-history/view/<int:child_id>/', views.view_medical_history, name='view_medical_history')

]