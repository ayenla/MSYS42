from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import models
from django import forms
from .models import *
from .forms import *
from datetime import date, datetime
from django.db.models import Q

from .forms import MedicalHistoryForm, ImmunizationForm
from django.forms import inlineformset_factory
def home(request):
    query = request.GET.get('q', '')
    
    if query:
        # Search for child by code or name (case-insensitive, partial match)
        children = Child.objects.filter(
            Q(code__icontains=query) |
            Q(lastname__icontains=query) |
            Q(firstname__icontains=query) |
            Q(middlename__icontains=query)
        )
    else:
        children = Child.objects.all()
    
    numbers = ContactNumber.objects.all()
    
    # Check if it's an AJAX request
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    return render(request, 'msys42app/home.html', {
        'children': children, 
        'contacts': numbers,
        'search_query': query,
        'is_ajax': is_ajax
    })

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

#Family Medical Records
def view_family_medicals(request, pk): 
    child = get_object_or_404(Child, pk=pk)
    members = FamilyMember.objects.filter(child=child)
    
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        middlename = request.POST.get('middlename')
        relationship = request.POST.get('relationship')
        sex = request.POST.get('sex')
    
        member = FamilyMember.objects.create(
            child=child, fm_firstname=firstname, fm_lastname=lastname, 
            fm_middlename=middlename, fm_relationship=relationship,
            fm_sex=sex
        )
        member.save() 
        return render(request, 'msys42app/home_family_medical.html', {'child': child, 'members': members})
    
    return render(request, 'msys42app/home_family_medical.html', {'child': child, 'members': members})

def view_family_medical_record(request, pk, id):
    child = get_object_or_404(Child, pk=pk)
    member = get_object_or_404(FamilyMember, pk=id)
    records = FamilyMedicalRecord.objects.filter(member=member)

    return render(request, 'msys42app/view_family_medical_records.html', {'child': child, 'member':member, 'records':records})

def edit_family_medical_record(request, pk, id):
    child = get_object_or_404(Child, pk=pk)
    member = get_object_or_404(FamilyMember, pk=id)
    records = FamilyMedicalRecord.objects.filter(member=member)
    
    if request.method == "POST":
        # Assuming multiple new records are submitted
        dates = request.POST.getlist('records[][date]')
        ages = request.POST.getlist('records[][age]')
        heights = request.POST.getlist('records[][height]')
        weights = request.POST.getlist('records[][weight]')
        bmis = request.POST.getlist('records[][bmi]')
        bps = request.POST.getlist('records[][bp]')
        temps = request.POST.getlist('records[][temperature]')
        statuses = request.POST.getlist('records[][medical_status]')
        meds = request.POST.getlist('records[][medication]')
        remarks = request.POST.getlist('records[][remarks]')

        print(temps)
        print(statuses)

        for i in range(len(dates)):
            record = FamilyMedicalRecord.objects.create(
                member=member,
                date=dates[i],
                age=ages[i],
                height=heights[i],
                weight=weights[i],
                bmi=bmis[i],
                bp=bps[i],
                temp=temps[i],
                med_stat=statuses[i],
                medication=meds[i],
                remarks=remarks[i]
            )
            print(record)
        return render(request, 'msys42app/view_family_medical_records.html', {'child': child, 'member':member, 'records':records})
    

    return render(request, 'msys42app/edit_family_medical.html', {'child': child, 'member':member, 'records':records})

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
                
                # Handle other_condition field
                other_condition = form.cleaned_data.get('other_condition', '')
                selected_allergies = form.cleaned_data.get('allergies_conditions', [])
                if 'other' in selected_allergies and other_condition:
                    medical_history.other_condition = other_condition
                elif 'other' not in selected_allergies:
                    medical_history.other_condition = ''
                
                medical_history.save()

                # Handle allergies
                medical_history.allergies_conditions.clear()  # Clear existing allergies
                
                # First add all allergies except "other"
                for allergy_code in selected_allergies:
                    if allergy_code != 'other':
                        allergy, _ = AllergyCondition.objects.get_or_create(name=dict(ALLERGY_CHOICES)[allergy_code])
                        medical_history.allergies_conditions.add(allergy)
                
                # Then add "other" if it exists (so it's at the end)
                if 'other' in selected_allergies:
                    allergy, _ = AllergyCondition.objects.get_or_create(name="Others")
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
                
                return redirect('view_medical_history', child_id=child.id)
            except Exception as e:
                print(f"Error saving data: {str(e)}")
                messages.error(request, f"Error saving data: {str(e)}")
        else:
            print("Form validation errors:", form.errors)
            for field, errors in form.errors.items():
                messages.error(request, f"{field}: {', '.join(errors)}")
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
            'allergies_conditions': existing_allergies,
            'other_condition': medical_history.other_condition
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
    all_years = list(range(datetime.now().year, 1899, -1))
    used_years = exams.values_list('year', flat=True)
    available_years = [y for y in all_years if y not in used_years]

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
        skin = request.POST.get('skin')
        nutrition = request.POST.get('nutrition')
        other_label = request.POST.get('other_label')
        other = request.POST.get('other')

        exam = PhysiciansExam.objects.create(
             child=child, year=year, grade=grade, height=height, weight=weight, bp=bp,
             vision_right=vision_right, vision_left=vision_left, hearing_right=hearing_right,
             hearing_left=hearing_left, eyes=eyes, ears=ears, nose=nose, throat=throat,
             teeth=teeth, heart=heart, lungs=lungs, abdomen=abdomen, nervous_system=nervous_system,
             skin=skin, nutrition=nutrition, other_label=other_label, other=other
         )
        exam.save()
        return render(request, 'msys42app/home_pe.html', {'child': child, 'exams':exams})

    return render(request, "msys42app/create_phyexam.html", {"child": child, "years": available_years, "exams":exams})


def annual_medical_check_list(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    medical_checks = AnnualMedicalCheck.objects.filter(child=child)
    return render(request, 'msys42app/annual_medical_check_list.html', {
        'child': child,
        'medical_checks': medical_checks
    })

def create_annual_medical_check(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    if request.method == 'POST':
        form = AnnualMedicalCheckForm(request.POST)
        if form.is_valid():
            try:
                medical_check = form.save(commit=False)
                medical_check.child = child
                medical_check.save()
                return redirect('annual_medical_check_list', child_id=child_id)
            except Exception as e:
                print(f"Error saving medical check: {str(e)}")
                messages.error(request, f"Error saving medical check: {str(e)}")
        else:
            print("Form validation errors:", form.errors)
            for field, errors in form.errors.items():
                messages.error(request, f"{field}: {', '.join(errors)}")
    else:
        form = AnnualMedicalCheckForm()
    return render(request, 'msys42app/create_annual_medical_check.html', {
        'form': form,
        'child': child
    })

def view_annual_medical_check(request, child_id, year):
    child = get_object_or_404(Child, id=child_id)
    medical_checks = AnnualMedicalCheck.objects.filter(
        child=child,
        date__year=year
    ).order_by('date')
    
    return render(request, 'msys42app/view_annual_medical_check.html', {
        'child': child,
        'year': year,
        'medical_checks': medical_checks
    })

def edit_annual_medical_check(request, child_id, check_id):
    child = get_object_or_404(Child, id=child_id)
    medical_check = get_object_or_404(AnnualMedicalCheck, id=check_id, child=child)
    
    if request.method == 'POST':
        form = AnnualMedicalCheckForm(request.POST, instance=medical_check)
        if form.is_valid():
            try:
                form.save()
                return redirect('view_annual_medical_check', child_id=child_id, year=medical_check.date.year)
            except Exception as e:
                print(f"Error updating medical check: {str(e)}")
                messages.error(request, f"Error updating medical check: {str(e)}")
        else:
            print("Form validation errors:", form.errors)
            for field, errors in form.errors.items():
                messages.error(request, f"{field}: {', '.join(errors)}")
    else:
        form = AnnualMedicalCheckForm(instance=medical_check)
    
    return render(request, 'msys42app/edit_annual_medical_check.html', {
        'form': form,
        'child': child,
        'medical_check': medical_check
    })

def delete_annual_medical_check(request, child_id, check_id):
    child = get_object_or_404(Child, id=child_id)
    medical_check = get_object_or_404(AnnualMedicalCheck, id=check_id, child=child)
    
    try:
        medical_check.delete()
    except Exception as e:
        print(f"Error deleting medical check: {str(e)}")
        messages.error(request, f"Error deleting medical check: {str(e)}")
        
    return redirect('annual_medical_check_list', child_id=child_id)
