from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import models
from django import forms
from .models import *
from .forms import *
from datetime import date, datetime

from .forms import MedicalHistoryForm, ImmunizationForm
from django.forms import inlineformset_factory
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

# START OF MEDICAL HISTORY
# Create formset for Immunization
ImmunizationFormSet = inlineformset_factory(
    MedicalHistory, 
    Immunization, 
    form=ImmunizationForm, 
    extra=0,
    can_delete=True,
    validate_min=False,
    validate_max=False
)

def add_medical_history(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    medical_history, created = MedicalHistory.objects.get_or_create(child=child)

    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST, instance=medical_history)
        immunization_formset = ImmunizationFormSet(request.POST, instance=medical_history, prefix='immunization')

        if form.is_valid() and immunization_formset.is_valid():
            try:
                # Save the main form
                medical_history = form.save(commit=False)
                medical_history.child = child
                medical_history.save()

                # Handle allergies
                medical_history.allergies_conditions.clear()  # Clear existing allergies
                selected_allergies = form.cleaned_data.get('allergies_conditions', [])
                for allergy_code in selected_allergies:
                    allergy, _ = AllergyCondition.objects.get_or_create(name=dict(ALLERGY_CHOICES)[allergy_code])
                    medical_history.allergies_conditions.add(allergy)
                
                # Save immunizations
                immunizations = immunization_formset.save(commit=False)
                
                # Delete any marked for deletion
                for obj in immunization_formset.deleted_objects:
                    obj.delete()
                
                # Save only non-empty immunizations
                for immunization in immunizations:
                    if immunization.date or immunization.immunization_given:  # Save if either field is filled
                        immunization.medical_history = medical_history
                        immunization.save()
                
                messages.success(request, "Medical history successfully updated!")
                return redirect('view_medical_history', child_id=child.id)
            except Exception as e:
                messages.error(request, f"Error saving data: {str(e)}")
                print(f"Error saving data: {str(e)}")
        else:
            messages.error(request, "There was an error updating medical history. Please check the form.")
            print("Form errors:", form.errors)
            print("Formset errors:", immunization_formset.errors)

    else:  # GET request
        # Get existing allergies and convert them to choice codes
        existing_allergies = [
            next(code for code, name in ALLERGY_CHOICES if name == allergy.name)
            for allergy in medical_history.allergies_conditions.all()
        ]
        
        # Initialize form with existing data including allergies
        initial_data = {
            'medical_status': medical_history.medical_status,
            'medical_status_history': medical_history.medical_status_history,
            'disability_status': medical_history.disability_status,
            'disability_status_history': medical_history.disability_status_history,
            'allergies_history': medical_history.allergies_history,
            'allergies_conditions': existing_allergies
        }
        form = MedicalHistoryForm(instance=medical_history, initial=initial_data)
        immunization_formset = ImmunizationFormSet(instance=medical_history, prefix='immunization')

    return render(request, 'msys42app/create_medhist.html', {
        'form': form,
        'immunization_formset': immunization_formset,
        'child': child
    })


def view_medical_history(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    medical_history, created = MedicalHistory.objects.get_or_create(child=child)
    immunizations = medical_history.immunizations.all()  # Use related_name to fetch related immunizations

    return render(request, 'msys42app/view_medhist.html', {
        'medical_history': medical_history,
        'immunizations': immunizations,
        'child': child
    })
# END OF MEDICAL HISTORY

#Start of Physician's Exams
def home_physicians_exam(request, pk):
    child = get_object_or_404(Child, pk=pk)
    exams = PhysiciansExam.objects.filter(child=child)
    return render(request, 'msys42app/home_pe.html', {'child': child, 'exams':exams})

def view_physicians_exam(request, pk, id):
    child = get_object_or_404(Child, pk=pk)
    exam = get_object_or_404(PhysiciansExam, pk=id)
    return render(request, 'msys42app/view_phyexam.html', {'child': child, 'exam':exam })

def create_physicians_exam(request, pk):
    child = get_object_or_404(Child, pk=pk)
    exams = PhysiciansExam.objects.filter(child=child)
    years = list(range(datetime.now().year, 1899, -1))  # Generate a list of years

    if request.method == "POST":
        year = request.POST.get('year')
        grade = request.POST.get('grade')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        bp = request.POST.get('bp')
        vision_right = request.POST.get('vision_right')
        vision_left = request.POST.get('vision_left')
        hearing_right = request.POST.get('hearing_right')
        hearing_left = request.POST.get('hearing_left')
        eyes = request.POST.get('eyes')
        ears = request.POST.get('ears')
        nose = request.POST.get('nose')
        throat = request.POST.get('throat')
        teeth = request.POST.get('teeth')
        heart = request.POST.get('heart')
        lungs = request.POST.get('lungs')
        abdomen = request.POST.get('abdomen')
        nervous_system = request.POST.get('nervous_system')
        skin = request.POST.get('skin')
        nutrition = request.POST.get('nutrition')

        exam = PhysiciansExam.objects.create(
             child=child, year=year, grade=grade, height=height, weight=weight, bp=bp,
             vision_right=vision_right, vision_left=vision_left, hearing_right=hearing_right,
             hearing_left=hearing_left, eyes=eyes, ears=ears, nose=nose, throat=throat,
             teeth=teeth, heart=heart, lungs=lungs, abdomen=abdomen, nervous_system=nervous_system,
             skin=skin, nutrition=nutrition
         )
        exam.save()
        return render(request, 'msys42app/home_pe.html', {'child': child, 'exams':exams})

    return render(request, "msys42app/create_phyexam.html", {"child": child, "years": years, "exams":exams})
