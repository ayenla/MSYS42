from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from datetime import date

def home(request):
    children = Child.objects.all()
    numbers = ContactNumber.objects.all()
    return render(request, 'msys42app/home.html', {'children': children, 'contacts':numbers })

def view_child_profile(request, pk):
    child = get_object_or_404(Child, pk=pk)
    numbers = ContactNumber.objects.filter(child=child)
    return render(request, 'msys42app/view_cp.html', {'child': child, 'contacts':numbers })

def edit_child_profile(request,pk):
    child = get_object_or_404(Child, pk=pk)
    numbers = ContactNumber.objects.filter(child=child)

    return render(request, 'msys42app/edit_cp.html', {'child': child, 'contacts':numbers })


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
        guardian_lastname = request.POST.get('guardian_lastname')
        guardian_firstname = request.POST.get('guardian_firstname')
        guardian_middlename = request.POST.get('guardian_middlename')
        guardian_relationship = request.POST.get('relationship')
        guardian_sex = request.POST.get('guardian_sex')
        contact_numbers = request.POST.getlist('contact_number[]') 

        birth_date = date.fromisoformat(birth)
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        

        if Child.objects.filter(code=code).exists():
            error_message = 'SPC Code already taken.'

            return render(request, 'msys42app/create_cp.html', {'error_message_var':error_message, 'code':code, 'lastname':lastname, 'firstname':firstname, 'middlename':middlename, 'sex':sex, 'birth':birth, 'blood_group':blood_group, 'address':address, 'philhealth':philhealth_number, 'fourps':fourps_number, 'guardian_lastname':guardian_lastname, 'guardian_firstname':guardian_firstname, 'guardian_middlename':guardian_middlename, 'guardian_relationship':guardian_relationship, 'guardian_sex':guardian_sex, 'phone':contact_numbers})
        
        if (philhealth_number and not philhealth_number.replace("-", "").isdigit()) or (fourps_number and not fourps_number.isdigit()):
            error_message = "Only numerical digits are allowed for PhilHealth Number and 4P's Number."
            return render(request, 'msys42app/create_cp.html', {'error_message_var':error_message, 'code':code, 'lastname':lastname, 'firstname':firstname, 'middlename':middlename, 'sex':sex, 'birth':birth, 'blood_group':blood_group, 'address':address, 'philhealth':philhealth_number, 'fourps':fourps_number, 'guardian_lastname':guardian_lastname, 'guardian_firstname':guardian_firstname, 'guardian_middlename':guardian_middlename, 'guardian_relationship':guardian_relationship, 'guardian_sex':guardian_sex, 'phone':contact_numbers})
        

      
        child = Child.objects.create(
            code=code, lastname=lastname, firstname=firstname, middlename=middlename,
            sex=sex, birth=birth, blood_group=blood_group, address=address,
            philhealth_number=philhealth_number, fourps_number=fourps_number,
            guardian_lastname=guardian_lastname, guardian_firstname=guardian_firstname, 
            guardian_middlename=guardian_middlename, guardian_relationship=guardian_relationship,
            guardian_sex=guardian_sex, age=age
        )

        childnum = Child.objects.get(pk=child.pk)

        for phone in contact_numbers:
            if phone.strip():  
                ContactNumber.objects.create(child=childnum, number=phone)

        return redirect('home') 

    return render(request, 'msys42app/create_cp.html')
