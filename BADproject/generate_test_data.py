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

from msys42app.models import Child, ContactNumber, FamilyMember, MedicalHistory, AllergyCondition, Immunization

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

def generate_random_date(start_year=2015, end_year=2023):
    """Generate a random date for immunization records"""
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    # Make sure we don't generate invalid dates like February 30
    max_day = 28 if month == 2 else 30 if month in [4, 6, 9, 11] else 31
    day = random.randint(1, max_day)
    return date(year, month, day)

def generate_medical_history(child):
    """Generate medical history for a child"""
    # Create medical history record
    medical_statuses = [
        "Good health", 
        "Regular check-ups required", 
        "Under medication", 
        "Recovering from illness", 
        "Needs regular monitoring",
        ""
    ]
    
    disability_statuses = [
        "None",
        "Minor physical disability",
        "Learning disability",
        "Hearing impairment",
        "Visual impairment",
        ""
    ]
    
    # Define common medical histories
    med_histories = [
        "No significant medical history",
        "Received regular vaccinations",
        "Had minor childhood illnesses",
        f"Had {fake.word()} surgery in {random.randint(2015, 2022)}",
        f"Hospitalized for {fake.word()} in {random.randint(2015, 2022)}",
        "Has occasional respiratory issues",
        "Prone to seasonal allergies",
        f"Diagnosed with {fake.word()} at age {random.randint(2, 10)}",
        ""
    ]
    
    # Define disability histories
    dis_histories = [
        "No disability history",
        f"Diagnosed with {fake.word()} at age {random.randint(2, 10)}",
        "Requires special education support",
        "Uses assistive devices",
        "Receiving therapy sessions",
        ""
    ]
    
    # Define allergy histories
    allergy_histories = [
        "No known allergies",
        f"Allergic to {fake.word()} since {random.randint(2015, 2022)}",
        "Seasonal allergies during summer",
        "Mild food allergies",
        "Occasional skin reactions",
        ""
    ]
    
    # Specific medical conditions for "other" field
    other_conditions = [
        "Tonsillitis", 
        "Sinusitis", 
        "Tuberculosis", 
        "Scabies", 
        "Gastroenteritis", 
        "UTI"
    ]
    
    # ALLERGY_CHOICES as defined in models.py
    ALLERGY_CHOICES = [
        ("arthritis", "IRA Arthritic"),
        ("asthma", "Asthma"),
        ("behavioral_problem", "Behavioral Problem"),
        ("cancer", "Cancer"),
        ("chronic_cough", "Chronic Cough/Wheezing"),
        ("diabetes", "Diabetes"),
        ("hearing_problem", "Hearing Problem"),
        ("heart_disease", "Heart Disease"),
        ("hypertension", "Hypertension"),
        ("jaundice", "Jaundice"),
        ("malaria", "Malaria"),
        ("seizures", "Seizures"),
        ("sickle_cell_anemia", "Sickle Cell Anemia"),
        ("skin_problem", "Skin Problem"),
        ("vision_problem", "Vision Problem"),
        ("other", "Others"),
    ]
    
    # Common immunizations
    immunizations = [
        "BCG",
        "Hepatitis B",
        "DTaP",
        "Haemophilus influenzae type b (Hib)",
        "Polio (IPV)",
        "Pneumococcal (PCV)",
        "Rotavirus",
        "Measles, Mumps, Rubella (MMR)",
        "Varicella (Chickenpox)",
        "Hepatitis A",
        "Typhoid",
        "Dengue",
        "COVID-19",
        "Flu Vaccine"
    ]
    
    # Create medical history record
    med_history = MedicalHistory.objects.create(
        child=child,
        med_stat=random.choice(medical_statuses),
        med_history=random.choice(med_histories),
        dis_stat=random.choice(disability_statuses),
        dis_history=random.choice(dis_histories),
        allergies_history=random.choice(allergy_histories),
        other_condition="" if random.random() > 0.1 else random.choice(other_conditions)
    )
    
    # Randomly add allergies (0-3)
    num_allergies = random.randint(0, 3)
    if num_allergies > 0:
        selected_allergies = random.sample([code for code, _ in ALLERGY_CHOICES if code != "other"], num_allergies)
        
        # Small chance to add "other" allergy
        if random.random() < 0.1:
            selected_allergies.append("other")
            med_history.other_condition = random.choice(other_conditions)
            med_history.save()
        
        # Add allergies to medical history
        for allergy_code in selected_allergies:
            allergy_name = dict(ALLERGY_CHOICES)[allergy_code]
            allergy, _ = AllergyCondition.objects.get_or_create(name=allergy_name)
            med_history.allergies_conditions.add(allergy)
    
    # Randomly add immunizations (1-5)
    num_immunizations = random.randint(1, 5)
    for _ in range(num_immunizations):
        Immunization.objects.create(
            medical_history=med_history,
            date=generate_random_date(),
            immunization_given=random.choice(immunizations)
        )
    
    return med_history

def generate_child_profiles(num_profiles=2000):
    """Generate specified number of child profiles"""
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', None]
    relationships = ['Mother', 'Father', 'Grandmother', 'Grandfather', 'Aunt', 'Uncle', 'Guardian']
    
    for i in range(num_profiles):
        try:
            # Generate unique SPC code
            while True:
                spc_code = generate_spc_code()
                if not Child.objects.filter(spc_code=spc_code).exists():
                    break
            
            # Generate child's data
            last_name = fake.last_name()
            first_name = fake.first_name()
            middle_name = fake.first_name()
            sex = random.choice(['Male', 'Female'])
            dob = generate_birth_date()
            age = calculate_age(dob)
            blood_grp = random.choice(blood_groups)
            comm_address = fake.address()
            
            # Generate guardian's data
            guardian_lastname = fake.last_name()
            guardian_firstname = fake.first_name()
            guardian_middlename = fake.first_name()
            guardian_relationship = random.choice(relationships)
            guardian_sex = random.choice(['Male', 'Female'])
            
            # Create child profile
            child = Child.objects.create(
                spc_code=spc_code,
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
                sex=sex,
                dob=dob,
                blood_grp=blood_grp,
                comm_address=comm_address,
                fam_philhealth=None,  # Optional
                fam_4ps=None,      # Optional
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
                last_name=guardian_lastname,
                first_name=guardian_firstname,
                middle_name=guardian_middlename,
                relationship_w_spc=guardian_relationship,
                sex=guardian_sex
            )
            
            # Generate medical history for the child
            generate_medical_history(child)
            
            print(f"Created profile {i+1}/{num_profiles}: {spc_code} - {first_name} {last_name}")
        except Exception as e:
            print(f"Error creating profile {i+1}: {str(e)}")
            continue

if __name__ == '__main__':
    generate_child_profiles() 