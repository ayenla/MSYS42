from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator 
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

# User Profile model to extend the default User model
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('medical_staff', 'Medical Staff'),
        ('program_coordinator', 'Program Coordinator'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='program_coordinator')
    
    def is_medical_staff(self):
        return self.role == 'medical_staff' or self.role == 'admin'
    
    def is_program_coordinator(self):
        return self.role == 'program_coordinator'
    
    def is_admin(self):
        return self.role == 'admin' or self.user.is_superuser
        
    class Meta:
        db_table = 'user_profiles'

class Child(models.Model):
    spc_code = models.CharField(max_length=7, validators=[RegexValidator(regex=r'^[A-Za-z]{3}\d{4}$')], unique=True, null=False, blank=False)
    last_name = models.CharField(max_length=25, null=False, blank=False)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    middle_name = models.CharField(max_length=25, null=True)
    sex = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female')], null=False, blank=False)
    dob = models.DateField(null=False, blank=False)
    blood_grp = models.CharField(max_length=3, blank=True, null=True)
    comm_address = models.TextField(max_length=255, null=False, blank=False)
    fam_philhealth = models.CharField(max_length=14, validators=[MinLengthValidator(14)], blank=True, null=True)
    fam_4ps = models.CharField(max_length=20, blank=True, null=True)
    guardian_lastname = models.CharField(max_length=25, null=False, blank=False)
    guardian_firstname = models.CharField(max_length=50, null=False, blank=False)
    guardian_middlename = models.CharField(max_length=25, null=True, blank=True)
    guardian_relationship = models.CharField(max_length=25, null=False, blank=False)
    guardian_sex = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female')], null=False, blank=False)
    age = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.pk}: {self.spc_code} {self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'spc'
    
class Education(models.Model):
    grades = [
    ("Preparatory", "Preparatory"),
    ("Grade 1", "Grade 1"),
    ("Grade 2", "Grade 2"),
    ("Grade 3", "Grade 3"),
    ("Grade 4", "Grade 4"),
    ("Grade 5", "Grade 5"),
    ("Grade 6", "Grade 6"),
    ("Grade 7", "Grade 7"),
    ("Grade 8", "Grade 8"),
    ("Grade 9", "Grade 9"),
    ("Grade 10", "Grade 10"),
    ("Grade 11", "Grade 11"),
    ("Grade 12", "Grade 12"),
    ("NE", "Not Evaluated"),
    ("Higher Education", "Higher Education"),
]
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    year = models.CharField(max_length=9, blank=True, null=True)
    grade = models.CharField(max_length= 25, blank=True, null=True, choices=grades)

    def __str__(self):
        return f"{self.child.first_name} {self.child.last_name}: {self.year}: {self.grade}"

    class Meta:
        db_table = 'spc_ed'

class ContactNumber(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name="phone_numbers")
    number = models.CharField(max_length=11)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['child', 'number'], name='unique_child_number')
        ]

    def __str__(self):
        return f"{self.pk}: {self.child.first_name} {self.child.last_name} - {self.number}"
    
class FamilyMember(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=25, null=False, blank=False)
    first_name = models.CharField(max_length=25, null=False, blank=False)
    middle_name = models.CharField(max_length=25, null=True, blank=False)
    relationship_w_spc = models.CharField(max_length=25, null=False, blank=False)
    sex = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female')], null=False, blank=False)
    
    def __str__(self):
        return f"{self.child.spc_code}: {self.relationship_w_spc} {self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'fam_member'
    
class FamilyMedicalRecord(models.Model):
    member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False) 
    age = models.PositiveSmallIntegerField(null=True, blank=True)  
    height = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True) 
    weight = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    bp = models.CharField(max_length=7, null=True, blank=True)
    temp = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    med_stat = models.CharField(max_length=50, null=True, blank=True)
    medication = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.member.first_name} {self.member.last_name},:  {self.date}"
    
    class Meta:
        db_table = 'fam_med_record'

    
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
    med_stat = models.CharField(max_length=255)
    med_history = models.CharField(max_length=255)
    dis_stat = models.CharField(max_length=255)
    dis_history = models.CharField(max_length=255)
    allergies_conditions = models.ManyToManyField('AllergyCondition', blank=True)
    allergies_history = models.CharField(max_length=255)
    other_condition = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'spc_med_hist'

class AllergyCondition(models.Model):
    name = models.CharField(max_length=100, unique=True) 
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'spc_cond'

class Immunization(models.Model):
    medical_history = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE, related_name='immunizations')
    date = models.DateField()
    immunization_given = models.CharField(max_length=50)

    class Meta:
        db_table = 'spc_im'

# END OF MEDICAL HISTORY

# PHYSICIAN EXAM SECTION
class PhysiciansExam(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    year_choices = [(year, year) for year in range(2000, datetime.datetime.now().year + 1)]
    conditions = [("N", "N"), ("A", "A"), ("C", "C"), ("R", "R"), ("NE", "NE")]
    year = models.IntegerField(choices=year_choices, default=datetime.datetime.now().year)
    # grade = models.CharField(max_length=2, choices=conditions, default= "NE")
    height = models.CharField(max_length=2, choices=conditions, default= "NE")
    weight = models.CharField(max_length=2, choices=conditions, default= "NE")
    bp = models.CharField(max_length=2, choices=conditions, default= "NE")
    vision_r = models.CharField(max_length=2, choices=conditions, default= "NE")
    vision_l = models.CharField(max_length=2, choices=conditions, default= "NE")
    hearing_r = models.CharField(max_length=2, choices=conditions, default= "NE")
    hearing_l = models.CharField(max_length=2, choices=conditions, default= "NE")
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

    def __str__(self):
        return f"{self.child.spc_code}: {self.year}"
    
    class Meta:
        db_table = 'phys_exam'

class PhysiciansExamOther(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    conditions = [("N", "N"), ("A", "A"), ("C", "C"), ("R", "R"), ("NE", "NE")]
    year = models.IntegerField(default=datetime.datetime.now().year)
    condition = models.CharField(max_length=2, choices=conditions, default= "NE", null=False, blank=False)
    attribute = models.CharField(max_length=20, default="other", null=False, blank=False)

    def __str__(self):
        return f"{self.child.spc_code}: {self.year}"
    
    class Meta:
        db_table = 'phys_exam_other'

#END PHYSICIAN'S EXAM

class AnnualMedicalCheck(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='annual_medical_checks')
    date = models.DateField()
    height = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)  # in cm
    weight = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)  # in kg
    bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hemoglobin = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
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
        return f"Medical Check for {self.child.first_name} {self.child.last_name} on {self.date}"

    class Meta:
        ordering = ['-date']  # Order by date in descending order (newest first)
        db_table = 'annual_med_check'
