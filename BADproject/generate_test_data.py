import os
import sys
import django
import random
from datetime import date, timedelta
from faker import Faker


#TO RUN: python generate_test_data.py #################
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BADproject.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from msys42app.models import Child, ContactNumber, FamilyMember

fake = Faker()

def generate_spc_code():
    """Generate a valid SPC code (3 letters followed by 4 digits)"""
    letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
    numbers = ''.join(random.choices('0123456789', k=4))
    return f"{letters}{numbers}"

def generate_phone_number():
    """Generate a valid Philippine phone number"""
    return f"09{random.randint(100000000, 999999999)}"

def generate_birth_date():
    """Generate a birth date between 2000 and 2015"""
    start_date = date(2000, 1, 1)
    end_date = date(2015, 12, 31)
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    return start_date + timedelta(days=random_days)

def calculate_age(birth_date):
    """Calculate age based on birth date"""
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def generate_child_profiles(num_profiles=500):
    """Generate specified number of child profiles"""
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', None]
    relationships = ['Mother', 'Father', 'Grandmother', 'Grandfather', 'Aunt', 'Uncle', 'Guardian']
    
    for i in range(num_profiles):
        try:
            # Generate unique SPC code
            while True:
                code = generate_spc_code()
                if not Child.objects.filter(code=code).exists():
                    break
            
            # Generate child's data
            lastname = fake.last_name()
            firstname = fake.first_name()
            middlename = fake.first_name()
            sex = random.choice(['Male', 'Female'])
            birth = generate_birth_date()
            age = calculate_age(birth)
            blood_group = random.choice(blood_groups)
            address = fake.address()
            
            # Generate guardian's data
            guardian_lastname = fake.last_name()
            guardian_firstname = fake.first_name()
            guardian_middlename = fake.first_name()
            guardian_relationship = random.choice(relationships)
            guardian_sex = random.choice(['Male', 'Female'])
            
            # Create child profile
            child = Child.objects.create(
                code=code,
                lastname=lastname,
                firstname=firstname,
                middlename=middlename,
                sex=sex,
                birth=birth,
                blood_group=blood_group,
                address=address,
                philhealth_number=None,  # Optional
                fourps_number=None,      # Optional
                guardian_lastname=guardian_lastname,
                guardian_firstname=guardian_firstname,
                guardian_middlename=guardian_middlename,
                guardian_relationship=guardian_relationship,
                guardian_sex=guardian_sex,
                age=age
            )
            
            # Create contact numbers (1-3 numbers per child)
            num_contacts = random.randint(1, 3)
            for _ in range(num_contacts):
                ContactNumber.objects.create(
                    child=child,
                    number=generate_phone_number()
                )
            
            # Create family member record
            FamilyMember.objects.create(
                child=child,
                fm_lastname=guardian_lastname,
                fm_firstname=guardian_firstname,
                fm_middlename=guardian_middlename,
                fm_relationship=guardian_relationship,
                fm_sex=guardian_sex
            )
            
            print(f"Created profile {i+1}/{num_profiles}: {code} - {firstname} {lastname}")
        except Exception as e:
            print(f"Error creating profile {i+1}: {str(e)}")
            continue

if __name__ == '__main__':
    generate_child_profiles() 