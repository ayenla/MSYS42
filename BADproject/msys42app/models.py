from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator # added on 2/26/2025, 03:38
from django.utils import timezone

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
