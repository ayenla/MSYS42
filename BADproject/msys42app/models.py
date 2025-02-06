from django.db import models

# Create your models here.
class Child(models.Model):
    spc_code = models.CharField(max_length=300, unique=True, null=False)
    spc_name = models.CharField(max_length=300, null=False)
    spc_sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'),('Others','Others')], null=False)
    spc_birth = models.DateField(null=False)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    address = models.TextField(null=False)
    philhealth_number = models.CharField(max_length=50, blank=True, null=True)
    fourps_number = models.CharField(max_length=50, blank=True, null=True)
    guardian_name = models.CharField(max_length=300, null=False)
    guardian_relationship = models.CharField(max_length=100, null=False)
    guardian_sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'),('Others','Others')], null=False)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
