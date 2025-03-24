from django.contrib import admin
from .models import Child, ContactNumber
#UN: tanseis
#PW: msys42
admin.site.register(Child)
admin.site.register(ContactNumber)
admin.site.register(PhysiciansExam)
admin.site.register(Immunization)
admin.site.register(AllergyCondition)
admin.site.register(MedicalHistory)

