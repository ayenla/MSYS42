from django.shortcuts import render, redirect
from .models import *
from datetime import date

def home(request):
    children = Child.objects.all()
    numbers = ContactNumber.objects.all()
    return render(request, 'msys42app/home.html', {'children': children, 'contacts':numbers })

def create_child_profile(request):
    children = Child.objects.all()
    numbers = ContactNumber.objects.all()
    if request.method == 'POST':
        code = request.POST.get('code')
        lastname = request.POST.get('lastname')
        firstname = request.POST.get('firstname')
        middlename = request.POST.get('middlename')
        sex = request.POST.get('sex')
        birth = request.POST.get('birth')
        blood_group = request.POST.get('blood_group')
        address = request.POST.get('address')
        philhealth_number = request.POST.get('philhealth')
        fourps_number = request.POST.get('fourps')
        guardian_name = request.POST.get('guardian_name')
        guardian_relationship = request.POST.get('relationship')
        guardian_sex = request.POST.get('guardian_sex')
        contact_numbers = request.POST.getlist('contact_number[]') 

        birth_date = date.fromisoformat(birth)
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        child = Child.objects.create(
            code=code, lastname=lastname, firstname=firstname, middlename=middlename,
            sex=sex, birth=birth, blood_group=blood_group, address=address,
            philhealth_number=philhealth_number, fourps_number=fourps_number,
            guardian_name=guardian_name, guardian_relationship=guardian_relationship,
            guardian_sex=guardian_sex, age=age
        )

        childnum = Child.objects.get(pk=child.pk)

        for phone in contact_numbers:
            if phone.strip():  
                
                ContactNumber.objects.create(child=childnum, number=phone)

        return render(request, 'msys42app/home.html', {'children': children, 'contacts':numbers })


    return render(request, 'msys42app/create_cp.html')
