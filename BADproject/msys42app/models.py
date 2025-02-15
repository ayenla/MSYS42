from django.db import models
from django.utils import timezone

class Child(models.Model):
    code = models.CharField(max_length=300, unique=True, null=False)
    lastname = models.CharField(max_length=300, null=True)
    firstname = models.CharField(max_length=300, null=True)
    middlename = models.CharField(max_length=300, null=True)
    sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], null=True)
    birth = models.DateField(null=False)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    address = models.TextField(null=False)
    philhealth_number = models.CharField(max_length=50, blank=True, null=True)
    fourps_number = models.CharField(max_length=50, blank=True, null=True)
    guardian_name = models.CharField(max_length=300, null=True)
    guardian_relationship = models.CharField(max_length=100, null=True)
    guardian_sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], null=True)
    age = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.code} {self.firstname} {self.lastname}"

class ContactNumber(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name="phone_numbers")
    number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.child.firstname} {self.child.lastname} - {self.number}"
