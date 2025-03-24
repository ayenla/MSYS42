from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator 
from django.utils import timezone
import datetime

class Child(models.Model):
    code = models.CharField(max_length=7, validators=[RegexValidator(regex=r'^[A-Za-z]{3}\d{4}$')], unique=True, null=False, blank=False)
    lastname = models.CharField(max_length=25, null=False, blank=False)
    firstname = models.CharField(max_length=50, null=False, blank=False)
    middlename = models.CharField(max_length=25, null=True)
    sex = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female')], null=False, blank=False)
    birth = models.DateField(null=False, blank=False)
    blood_group = models.CharField(max_length=3, blank=True, null=True)
    address = models.TextField(max_length=255, null=False, blank=False)
    philhealth_number = models.CharField(max_length=14, validators=[MinLengthValidator(14)], blank=True, null=True)
    fourps_number = models.CharField(max_length=20, blank=True, null=True)
    guardian_lastname = models.CharField(max_length=25, null=False, blank=False)
    guardian_firstname = models.CharField(max_length=50, null=False, blank=False)
    guardian_middlename = models.CharField(max_length=25, null=True, blank=True)
    guardian_relationship = models.CharField(max_length=25, null=False, blank=False)
    guardian_sex = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female')], null=False, blank=False)
    age = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.pk}: {self.code} {self.firstname} {self.lastname}"

class ContactNumber(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name="phone_numbers")
    number = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.pk}: {self.child.firstname} {self.child.lastname} - {self.number}"
    
# MEDICAL HISTORY SECTION

ALLERGY_CHOICES = [
    ("asthma", "Asthma"),
    ("behavioral_problem", "Behavioral Problem"),
    ("heart_disease", "Heart Disease"),
    ("hypertension", "Hypertension"),
    ("malaria", "Malaria"),
    ("cancer", "Cancer"),
    ("chronic_cough", "Chronic Cough/Wheezing"),
    ("arthritis", "IRA Arthritic"),
    ("seizures", "Seizures"),
    ("jaundice", "Jaundice"),
    ("diabetes", "Diabetes"),
    ("hearing_problem", "Hearing Problem"),
    ("sickle_cell_anemia", "Sickle Cell Anemia"),
    ("skin_problem", "Skin Problem"),
    ("vision_problem", "Vision Problem"),
]

class MedicalHistory(models.Model):
    child = models.OneToOneField(Child, on_delete=models.CASCADE)
    medical_status = models.CharField(max_length=255)
    medical_status_history = models.TextField()
    disability_status = models.CharField(max_length=255)
    disability_status_history = models.TextField()
    allergies_conditions = models.ManyToManyField('AllergyCondition', blank=True)
    allergies_history = models.TextField()

class AllergyCondition(models.Model):
    name = models.CharField(max_length=100, unique=True) 
    
    def __str__(self):
        return self.name

class Immunization(models.Model):
    medical_history = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE, related_name='immunizations')
    date = models.DateField()
    immunization_given = models.CharField(max_length=255)

# END OF MEDICAL HISTORY

# PHYSICIAN EXAM SECTION
class PhysiciansExam(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    year_choices = [(year, year) for year in range(2000, datetime.datetime.now().year + 1)]
    conditions = [("N", "N"), ("A", "A"), ("C", "C"), ("R", "R"), ("NE", "NE")]
    year = models.IntegerField(choices=year_choices, default=datetime.datetime.now().year)
    grade = models.CharField(max_length=2, choices=conditions, default= "NE")
    height = models.CharField(max_length=2, choices=conditions, default= "NE")
    weight = models.CharField(max_length=2, choices=conditions, default= "NE")
    bp = models.CharField(max_length=2, choices=conditions, default= "NE")
    vision_right = models.CharField(max_length=2, choices=conditions, default= "NE")
    vision_left = models.CharField(max_length=2, choices=conditions, default= "NE")
    hearing_right = models.CharField(max_length=2, choices=conditions, default= "NE")
    hearing_left = models.CharField(max_length=2, choices=conditions, default= "NE")
    eyes = models.CharField(max_length=2, choices=conditions, default= "NE")
    ears = models.CharField(max_length=2, choices=conditions, default= "NE")
    nose = models.CharField(max_length=2, choices=conditions, default= "NE")
    throat = models.CharField(max_length=2, choices=conditions, default= "NE")
    teeth = models.CharField(max_length=2, choices=conditions, default= "NE")
    heart = models.CharField(max_length=2, choices=conditions, default= "NE")
    lungs = models.CharField(max_length=2, choices=conditions, default= "NE")
    abdomen = models.CharField(max_length=2, choices=conditions, default= "NE")
    nervous_system = models.CharField(max_length=2, choices=conditions, default= "NE")
    skin = models.CharField(max_length=2, choices=conditions, default= "NE")
    nutrition = models.CharField(max_length=2, choices=conditions, default= "NE")
    other = models.CharField(max_length=2, choices=conditions, default= "NE")
    other_label = models.CharField(max_length=20, default="other")

#END PHYSICIAN'S EXAM
