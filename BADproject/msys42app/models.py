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
    
class FamilyMember(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    fm_lastname = models.CharField(max_length=25, null=False, blank=False)
    fm_firstname = models.CharField(max_length=25, null=False, blank=False)
    fm_middlename = models.CharField(max_length=25, null=True, blank=False)
    fm_relationship = models.CharField(max_length=25, null=False, blank=False)
    fm_sex = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female')], null=False, blank=False)
    
    def __str__(self):
        return f"{self.child}: {self.fm_relationship} {self.fm_firstname} {self.fm_lastname}"
    
class FamilyMedicalRecord(models.Model):
    member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False) 
    age = models.PositiveSmallIntegerField()  
    height = models.DecimalField(max_digits=4, decimal_places=1) 
    weight = models.DecimalField(max_digits=4, decimal_places=1)
    bmi = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    bp = models.CharField(max_length=5) 
    temp = models.DecimalField(max_digits=3, decimal_places=1)
    med_stat = models.CharField(max_length=50)
    medication = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.member.fm_firstname} {self.member.fm_lastname},:  {self.date}"

    
# MEDICAL HISTORY SECTION

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

class MedicalHistory(models.Model):
    child = models.OneToOneField(Child, on_delete=models.CASCADE)
    medical_status = models.CharField(max_length=255)
    medical_status_history = models.TextField()
    disability_status = models.CharField(max_length=255)
    disability_status_history = models.TextField()
    allergies_conditions = models.ManyToManyField('AllergyCondition', blank=True)
    allergies_history = models.TextField()
    other_condition = models.CharField(max_length=255, blank=True, null=True)

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

    def __str__(self):
        return f"{self.child}: {self.year} {self.child.lastname} - {self.number}"

#END PHYSICIAN'S EXAM

class AnnualMedicalCheck(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='annual_medical_checks')
    date = models.DateField()
    height = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)  # in cm
    weight = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)  # in kg
    bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hemoglobin = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    condition = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def calculate_bmi(self):
        if self.height and self.weight and self.height > 0 and self.weight > 0:
            # BMI = weight (kg) / (height (m))²
            height_in_meters = self.height / 100
            return round(self.weight / (height_in_meters * height_in_meters), 2)
        return None

    def save(self, *args, **kwargs):
        self.bmi = self.calculate_bmi()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Medical Check for {self.child.firstname} {self.child.lastname} on {self.date}"

    class Meta:
        ordering = ['-date']  # Order by date in descending order (newest first)
