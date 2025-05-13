import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BADproject.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from msys42app.models import Child

def delete_all_child_profiles():
    """Delete all child profiles from the database"""
    # Get count before deletion
    count = Child.objects.count()
    
    # Delete all child profiles
    # This will cascade to delete all related records including:
    # - ContactNumber
    # - FamilyMember 
    # - MedicalHistory (and its related Immunization records)
    # because of the on_delete=models.CASCADE in the model definitions
    Child.objects.all().delete()
    
    print(f"Successfully deleted {count} child profiles and all related records.")

if __name__ == '__main__':
    # Ask for confirmation
    confirm = input("Are you sure you want to delete ALL child profiles? This cannot be undone. (yes/no): ")
    
    if confirm.lower() == 'yes':
        delete_all_child_profiles()
    else:
        print("Operation cancelled.") 