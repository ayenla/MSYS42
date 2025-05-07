from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from datetime import date, datetime
from django.db.models import Q
import re

from django.forms import inlineformset_factory

# Add this function to get user permissions based on role
def get_user_permissions(user):
    """Get user permissions based on role"""
    if not user.is_authenticated:
        return {
            'can_edit': False,
            'can_delete': False,
            'can_create': False,
            'can_view': False,
        }
    
    # Get user profile or default to program coordinator (view-only)
    if hasattr(user, 'profile'):
        profile = user.profile
    else:
        # Fallback if no profile exists
        return {
            'can_edit': False,
            'can_delete': False,
            'can_create': False,
            'can_view': True,
        }
    
    # Set permissions based on role
    if profile.is_admin():
        return {
            'can_edit': True,
            'can_delete': True,
            'can_create': True,
            'can_view': True,
        }
    elif profile.is_medical_staff():
        return {
            'can_edit': True,
            'can_delete': True,
            'can_create': True,
            'can_view': True,
        }
    else:  # Program Coordinator
        return {
            'can_edit': False,
            'can_delete': False,
            'can_create': False,
            'can_view': True,
        }

def parse_input(value, data_type):
    """
    Parse input value to the specified data type.
    Returns None if parsing fails.
    """
    if not value or value.strip() == '':
        return None
        
    try:
        if data_type == "int":
            return int(value)
        elif data_type == "float":
            return float(value)
        else:
            return value
    except (ValueError, TypeError):
        return None

@login_required
def home(request):
    query = request.GET.get('q', '')
    
    if query:
        # Search for child by code or name (case-insensitive, partial match)
        children = Child.objects.filter(
            Q(spc_code__icontains=query) |
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query)
        )
    else:
        children = Child.objects.all()
    
    numbers = ContactNumber.objects.all()
    
    # Check if it's an AJAX request
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # Add user permissions to context
    context = {
        'children': children, 
        'contacts': numbers,
        'search_query': query,
        'is_ajax': is_ajax,
        'perms': get_user_permissions(request.user)
    }
    return render(request, 'msys42app/home.html', context)


@login_required
def view_child_profile(request, pk):
    child = get_object_or_404(Child, pk=pk)
    numbers = ContactNumber.objects.filter(child=child)
    education_list = Education.objects.filter(child=child)

    year_choices = get_school_year_choices()
    grade_choices = Education._meta.get_field('grade').choices

    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.child = child 
            education.save()
            return redirect('view_child_profile', pk=pk)
    else:
        form = EducationForm()

    return render(request, 'msys42app/view_cp.html', {
        'child': child,
        'contacts': numbers,
        'education': education_list,
        'form': form,
        'year_choices': year_choices,
        'grade_choices': grade_choices,
        'perms': get_user_permissions(request.user),
    })

@login_required
def edit_education(request, pk, id):
    child = get_object_or_404(Child, pk=pk)
    education = get_object_or_404(Education, pk=id)
    if request.method == 'POST':
        education.child = child
        education.year = request.POST.get('year')
        education.grade = request.POST.get('grade')
        education.save()
    return redirect('view_child_profile', pk=child.pk)

@login_required
def delete_education(request, pk, id):
    child = get_object_or_404(Child, pk=pk)
    education = get_object_or_404(Education, pk=id)

    education.delete()

    messages.error(request, "Education detail has been deleted successfully.")
    return redirect('view_child_profile', pk=pk) 


@login_required
def edit_child_profile(request,pk):
    child = get_object_or_404(Child, pk=pk)
    numbers = ContactNumber.objects.filter(child=child)
    fam_member = get_object_or_404(FamilyMember, child=child, first_name=child.guardian_firstname, last_name=child.guardian_lastname)

    if request.method == 'POST':
        # Check if this is a delete request
        if 'delete_profile' in request.POST:
            # Delete related records first to maintain database integrity
            ContactNumber.objects.filter(child=child).delete()
            
            # Delete family members and their medical records
            family_members = FamilyMember.objects.filter(child=child)
            for member in family_members:
                FamilyMedicalRecord.objects.filter(member=member).delete()
            family_members.delete()
            
            # Delete any other related records
            PhysiciansExam.objects.filter(child=child).delete()
            AnnualMedicalCheck.objects.filter(child=child).delete()
            
            # If there's a medical history, delete it
            try:
                medical_history = MedicalHistory.objects.get(child=child)
                Immunization.objects.filter(medical_history=medical_history).delete()
                medical_history.delete()
            except MedicalHistory.DoesNotExist:
                pass
                
            # Finally delete the child
            child.delete()
            
            return redirect('home')
        
        # Otherwise, proceed with the regular edit functionality
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

        

        if code!= child.spc_code and Child.objects.filter(spc_code=code).exists():
            error_message = 'SPC Code already taken.'

            return render(request, 'msys42app/edit_cp.html', {'error_message_var':error_message, 'child': child, 'code':code, 'lastname':lastname, 'firstname':firstname, 'middlename':middlename, 'sex':sex, 'birth':birth, 'blood_group':blood_group, 'address':address, 'philhealth':philhealth_number, 'fourps':fourps_number, 'guardian_lastname':guardian_lastname, 'guardian_firstname':guardian_firstname, 'guardian_middlename':guardian_middlename, 'guardian_relationship':guardian_relationship, 'guardian_sex':guardian_sex, 'phone':contact_numbers})
        
        if (philhealth_number and not philhealth_number.replace("-", "").isdigit()) or (fourps_number and not fourps_number.isdigit()):
            error_message = "Only numerical digits are allowed for PhilHealth Number and 4P's Number."
            return render(request, 'msys42app/edit_cp.html', {'error_message_var':error_message, 'child': child, 'code':code, 'lastname':lastname, 'firstname':firstname, 'middlename':middlename, 'sex':sex, 'birth':birth, 'blood_group':blood_group, 'address':address, 'philhealth':philhealth_number, 'fourps':fourps_number, 'guardian_lastname':guardian_lastname, 'guardian_firstname':guardian_firstname, 'guardian_middlename':guardian_middlename, 'guardian_relationship':guardian_relationship, 'guardian_sex':guardian_sex, 'phone':contact_numbers})
        
        ContactNumber.objects.filter(child=child).delete()
        for phone in contact_numbers:
            if phone.strip():
                ContactNumber.objects.create(child=child, number=phone)

        member = FamilyMember.objects.filter(pk=fam_member.pk).update(
            child=child, first_name=guardian_firstname, last_name=guardian_lastname, 
            middle_name=guardian_middlename, relationship_w_spc=guardian_relationship,
            sex=guardian_sex
        )
      
        child = Child.objects.filter(pk=pk).update(
            spc_code=code, last_name=lastname, first_name=firstname, middle_name=middlename,
            sex=sex, dob=birth, blood_grp=blood_group, comm_address=address,
            fam_philhealth=philhealth_number, fam_4ps=fourps_number,
            guardian_lastname=guardian_lastname, guardian_firstname=guardian_firstname, 
            guardian_middlename=guardian_middlename, guardian_relationship=guardian_relationship,
            guardian_sex=guardian_sex, age=age
        )

        print("YEAAAHHH")

        return redirect('view_child_profile', pk=pk)

    print("awwww")
    return render(request, 'msys42app/edit_cp.html', {'child': child, 'contacts':numbers })


@login_required
def create_child_profile(request):
    numbers = ContactNumber.objects.all()

    if request.method == 'POST':
        code = request.POST.get('code', '')
        last_name = request.POST.get('lastname', '')
        first_name = request.POST.get('firstname', '')
        middle_name = request.POST.get('middlename', '')
        sex = request.POST.get('sex', '')
        dob = request.POST.get('birth', '')
        blood_grp = request.POST.get('blood_group', '')
        comm_address = request.POST.get('address', '')
        fam_philhealth = request.POST.get('philhealth', '')
        fam_4ps = request.POST.get('fourps', '')
        guardian_lastname = request.POST.get('guardian_lastname', '')
        guardian_firstname = request.POST.get('guardian_firstname', '')
        guardian_middlename = request.POST.get('guardian_middlename', '')
        relationship = request.POST.get('relationship', '')
        guardian_sex = request.POST.get('guardian_sex', '')
        phone = request.POST.getlist('contact_number[]')

        birth_date = date.fromisoformat(dob)
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        

        if Child.objects.filter(spc_code=code).exists():
            error_message = 'SPC Code already taken.'
            return render(request, 'msys42app/create_cp.html', {
                'error_message_var': error_message,
                'code': code,
                'last_name': last_name,
                'first_name': first_name,
                'middle_name': middle_name,
                'sex': sex,
                'dob': dob,
                'blood_grp': blood_grp,
                'comm_address': comm_address,
                'fam_philhealth': fam_philhealth,
                'fam_4ps': fam_4ps,
                'guardian_lastname': guardian_lastname,
                'guardian_firstname': guardian_firstname,
                'guardian_middlename': guardian_middlename,
                'relationship': relationship,
                'guardian_sex': guardian_sex,
                'phone': phone,
                'today': date.today().isoformat(),
            })
        
        if (fam_philhealth and not fam_philhealth.replace("-", "").isdigit()) or (fam_4ps and not fam_4ps.isdigit()):
            error_message = "Only numerical digits are allowed for PhilHealth Number and 4P's Number."
            return render(request, 'msys42app/create_cp.html', {
                'error_message_var': error_message,
                'code': code,
                'last_name': last_name,
                'first_name': first_name,
                'middle_name': middle_name,
                'sex': sex,
                'dob': dob,
                'blood_grp': blood_grp,
                'comm_address': comm_address,
                'fam_philhealth': fam_philhealth,
                'fam_4ps': fam_4ps,
                'guardian_lastname': guardian_lastname,
                'guardian_firstname': guardian_firstname,
                'guardian_middlename': guardian_middlename,
                'relationship': relationship,
                'guardian_sex': guardian_sex,
                'phone': phone,
                'today': date.today().isoformat(),
            })
        
        # Validate Family 4Ps Number format
        if fam_4ps and not re.fullmatch(r'\d{12}', fam_4ps):
            error_message = "Family 4Ps Number must be exactly 12 digits."
            return render(request, 'msys42app/create_cp.html', {
                'error_message_var': error_message,
                'code': code,
                'last_name': last_name,
                'first_name': first_name,
                'middle_name': middle_name,
                'sex': sex,
                'dob': dob,
                'blood_grp': blood_grp,
                'comm_address': comm_address,
                'fam_philhealth': fam_philhealth,
                'fam_4ps': fam_4ps,
                'guardian_lastname': guardian_lastname,
                'guardian_firstname': guardian_firstname,
                'guardian_middlename': guardian_middlename,
                'relationship': relationship,
                'guardian_sex': guardian_sex,
                'phone': phone,
                'today': date.today().isoformat(),
            })
        
        # Validate Date of Birth is not in the future
        try:
            parsed_dob = datetime.strptime(dob, '%Y-%m-%d').date()
            if parsed_dob > date.today():
                error_message = "Birthday must be on or before the current date."
                return render(request, 'msys42app/create_cp.html', {
                    'error_message_var': error_message,
                    'code': code,
                    'last_name': last_name,
                    'first_name': first_name,
                    'middle_name': middle_name,
                    'sex': sex,
                    'dob': dob,
                    'blood_grp': blood_grp,
                    'comm_address': comm_address,
                    'fam_philhealth': fam_philhealth,
                    'fam_4ps': fam_4ps,
                    'guardian_lastname': guardian_lastname,
                    'guardian_firstname': guardian_firstname,
                    'guardian_middlename': guardian_middlename,
                    'relationship': relationship,
                    'guardian_sex': guardian_sex,
                    'phone': phone,
                    'today': date.today().isoformat(),
                })
        except ValueError:
            if dob:
                error_message = "Invalid date format for Date of Birth."
                return render(request, 'msys42app/create_cp.html', {
                    'error_message_var': error_message,
                    'code': code,
                    'last_name': last_name,
                    'first_name': first_name,
                    'middle_name': middle_name,
                    'sex': sex,
                    'dob': dob,
                    'blood_grp': blood_grp,
                    'comm_address': comm_address,
                    'fam_philhealth': fam_philhealth,
                    'fam_4ps': fam_4ps,
                    'guardian_lastname': guardian_lastname,
                    'guardian_firstname': guardian_firstname,
                    'guardian_middlename': guardian_middlename,
                    'relationship': relationship,
                    'guardian_sex': guardian_sex,
                    'phone': phone,
                    'today': date.today().isoformat(),
                })
        

        child = Child.objects.create(
            spc_code=code, last_name=last_name, first_name=first_name, middle_name=middle_name,
            sex=sex, dob=dob, blood_grp=blood_grp, comm_address=comm_address,
            fam_philhealth=fam_philhealth, fam_4ps=fam_4ps,
            guardian_lastname=guardian_lastname, guardian_firstname=guardian_firstname, 
            guardian_middlename=guardian_middlename, guardian_relationship=relationship,
            guardian_sex=guardian_sex, age=age
        )

        childnum = Child.objects.get(pk=child.pk)

        for phone in phone:
            if phone.strip():  
                ContactNumber.objects.create(child=childnum, number=phone)

        member = FamilyMember.objects.create(
            child=child, first_name=guardian_firstname, last_name=guardian_lastname, 
            middle_name=guardian_middlename, relationship_w_spc=relationship,
            sex=guardian_sex
        )
        member.save() 

        return redirect('view_child_profile', pk=childnum.pk)

    else:
        # GET request: send empty strings for all fields
        return render(request, 'msys42app/create_cp.html', {
            'code': '',
            'last_name': '',
            'first_name': '',
            'middle_name': '',
            'sex': '',
            'dob': '',
            'blood_grp': '',
            'comm_address': '',
            'fam_philhealth': '',
            'fam_4ps': '',
            'guardian_lastname': '',
            'guardian_firstname': '',
            'guardian_middlename': '',
            'relationship': '',
            'guardian_sex': '',
            'phone': ['']
        })

#Family Medical Records
@login_required
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
            child=child, first_name=firstname, last_name=lastname, 
            middle_name=middlename, relationship_w_spc=relationship,
            sex=sex
        )
        member.save() 
        messages.success(request, "New family member has been added.")
        return render(request, 'msys42app/home_family_medical.html', {
            'child': child, 
            'members': members,
            'perms': get_user_permissions(request.user),
        })
    
    return render(request, 'msys42app/home_family_medical.html', {
        'child': child, 
        'members': members,
        'perms': get_user_permissions(request.user),
    })

@login_required
def delete_family_member(request, pk, id):
    child = get_object_or_404(Child, pk=pk)
    member = get_object_or_404(FamilyMember, pk=id)

    family_count = FamilyMember.objects.filter(child=child).count()

    if family_count <= 1:
        messages.error(request, "Cannot delete. A child must have at least one family member.")
        return redirect('edit_family_medical_record', pk=pk, id=id)  

    
    FamilyMedicalRecord.objects.filter(member=member).delete()

    member.delete()

    messages.success(request, "Family member and their records were successfully deleted.")
    return redirect('view_family_medicals', pk=pk) 

@login_required
def view_family_medical_record(request, pk, id):
    child = get_object_or_404(Child, pk=pk)
    member = get_object_or_404(FamilyMember, pk=id)
    records = FamilyMedicalRecord.objects.filter(member=member)

    return render(request, 'msys42app/view_family_medical_records.html', {
        'child': child, 
        'member': member, 
        'records': records,
        'perms': get_user_permissions(request.user),
    })

@login_required
def edit_family_info(request, pk, id):
    child = get_object_or_404(Child, pk=pk)
    member = get_object_or_404(FamilyMember, pk=id)
    records = FamilyMedicalRecord.objects.filter(member=member)

    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        middlename = request.POST.get('middlename')
        relationship = request.POST.get('relationship')
        sex = request.POST.get('sex')

        member.first_name = firstname
        member.last_name = lastname
        member.middle_name = middlename
        member.relationship_w_spc = relationship
        member.sex = sex
        member.child = child
        member.save()

        print(f"{firstname} {lastname} {middlename} {relationship} {sex}")
        return render(request, 'msys42app/edit_family_medical.html', {'child': child, 'member': member, 'records': records})
    
    return render(request, 'msys42app/edit_family_medical.html', {'child': child, 'member': member, 'records': records})

@login_required
def edit_family_medical_record(request, pk, id):
    child = get_object_or_404(Child, pk=pk)
    member = get_object_or_404(FamilyMember, pk=id)
    records = FamilyMedicalRecord.objects.filter(member=member)
    
    if request.method == "POST":
        records.delete() # Clear existing records and only save what is submitted
        # Assuming multiple new records are submitted
        dates = request.POST.getlist('records[][date]')
        ages = request.POST.getlist('records[][age]')
        heights = request.POST.getlist('records[][height]')
        weights = request.POST.getlist('records[][weight]')
        bps = request.POST.getlist('records[][bp]')
        temps = request.POST.getlist('records[][temperature]')
        statuses = request.POST.getlist('records[][medical_status]')
        meds = request.POST.getlist('records[][medication]')
        remarks = request.POST.getlist('records[][remarks]')

        for i in range(len(dates)):
            try: 
                record = FamilyMedicalRecord.objects.create(
                member=member,
                date=dates[i],
                age=ages[i],
                height=heights[i],
                weight=weights[i],
                bp=bps[i],
                temp=temps[i],
                med_stat=statuses[i],
                medication=meds[i],
                remarks=remarks[i]
                )

            except ValueError:
                age = parse_input(ages[i],"int")
                height = parse_input(heights[i],"float")
                weight = parse_input(weights[i],"float")
                height = parse_input(heights[i],"int")
                temp = parse_input(temps[i],"int")        

                record = FamilyMedicalRecord.objects.create(
                member=member,
                date=dates[i],
                age=age,
                height=height,
                weight=weight,
                bp=bps[i],
                temp=temp,
                med_stat=statuses[i],
                medication=meds[i],
                remarks=remarks[i]
                )
        return redirect('view_family_medical_record', pk=pk, id=id)   
        
    return render(request, 'msys42app/edit_family_medical.html', {'child': child, 'member':member, 'records':records})

@login_required
def delete_family_medical_record(request, pk, id, rec):
    child = get_object_or_404(Child, pk=pk)
    member = get_object_or_404(FamilyMember, pk=id)
    records = FamilyMedicalRecord.objects.filter(member=member)
    record = get_object_or_404(FamilyMedicalRecord, pk=rec)
    
    FamilyMedicalRecord.objects.filter(pk=rec).delete()
    record.delete()

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


@login_required
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
            'medical_status': medical_history.med_stat,
            'medical_status_history': medical_history.med_history,
            'disability_status': medical_history.dis_stat,
            'disability_status_history': medical_history.dis_history,
            'allergies_history': medical_history.allergies_history,
            'allergies_conditions': existing_allergies,
            'other_condition': medical_history.other_condition
        }
        form = MedicalHistoryForm(instance=medical_history, initial=initial_data)
        immunization_formset = ImmunizationFormSet(instance=medical_history, prefix='immunization')

    return render(request, 'msys42app/create_medhist.html', {
        'form': form,
        'immunization_formset': immunization_formset,
        'child': child,
        'today': date.today().isoformat(),
    })


@login_required
def view_medical_history(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    medical_history, created = MedicalHistory.objects.get_or_create(child=child)
    immunizations = medical_history.immunizations.all()  # Use related_name to fetch related immunizations

    return render(request, 'msys42app/view_medhist.html', {
        'medical_history': medical_history,
        'immunizations': immunizations,
        'child': child,
        'today': date.today().isoformat(),
        'perms': get_user_permissions(request.user),
    })
# END OF MEDICAL HISTORY

#Start of Physician's Exams
@login_required
def home_physicians_exam(request, pk):
    child = get_object_or_404(Child, pk=pk)
    exams = PhysiciansExam.objects.filter(child=child).order_by('-year')
    return render(request, 'msys42app/home_pe.html', {
        'child': child, 
        'exams': exams,
        'perms': get_user_permissions(request.user),
    })

@login_required
def view_physicians_exam(request, pk, id):
    child = get_object_or_404(Child, pk=pk)
    exam = get_object_or_404(PhysiciansExam, pk=id)
    return render(request, 'msys42app/view_phyexam.html', {'child': child, 'exam':exam })

@login_required
def create_physicians_exam(request, pk):
    child = get_object_or_404(Child, pk=pk)
    exams = PhysiciansExam.objects.filter(child=child)
    all_years = list(range(datetime.now().year, 1899, -1))
    used_years = exams.values_list('year', flat=True)
    available_years = [y for y in all_years if y not in used_years]

    if request.method == "POST":
        year = request.POST.get('year')
        # grade = request.POST.get('grade')
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
        other_label = request.POST.get('other_label', '')
        other = request.POST.get('other', 'NE')
        clear_other = request.POST.get('clear_other', 'false')

        # Only set other and other_label if they are provided
        exam_data = {
            'child': child,
            'year': year,
            'height': height,
            'weight': weight,
            'bp': bp,
            'vision_r': vision_right,
            'vision_l': vision_left,
            'hearing_r': hearing_right,
            'hearing_l': hearing_left,
            'eyes': eyes,
            'ears': ears,
            'nose': nose,
            'throat': throat,
            'teeth': teeth,
            'heart': heart,
            'lungs': lungs,
            'abdomen': abdomen,
            'nervous_system': nervous_system,
            'skin': skin,
            'nutrition': nutrition,
            'other_label': None,
            'other': None
        }

        # Set other fields if provided and not empty
        if clear_other != 'true' and other_label and other_label.strip():
            exam_data['other_label'] = other_label
            exam_data['other'] = other

        # Create the main exam record
        exam = PhysiciansExam.objects.create(**exam_data)
        
        # Process any additional fields (this would require model changes to support)
        # For now, we'll just handle the main "other" field
        
        return redirect('home_physicians_exam', pk=child.pk)

    return render(request, "msys42app/create_phyexam.html", {"child": child, "years": available_years, "exams":exams})


@login_required
def annual_medical_check_list(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    medical_checks = AnnualMedicalCheck.objects.filter(child=child)
    return render(request, 'msys42app/annual_medical_check_list.html', {
        'child': child,
        'medical_checks': medical_checks,
        'perms': get_user_permissions(request.user),
    })

@login_required
def create_annual_medical_check(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    
    # Get existing years for this child
    existing_years = list(AnnualMedicalCheck.objects.filter(child=child)
                         .values_list('date__year', flat=True))
    
    if request.method == 'POST':
        form = AnnualMedicalCheckForm(request.POST, child=child)
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
        form = AnnualMedicalCheckForm(child=child)
    
    return render(request, 'msys42app/create_annual_medical_check.html', {
        'form': form,
        'child': child,
        'existing_years': existing_years,
        'today': date.today().isoformat(),
    })

@login_required
def view_annual_medical_check(request, child_id, year):
    child = get_object_or_404(Child, id=child_id)
    medical_checks = AnnualMedicalCheck.objects.filter(
        child=child,
        date__year=year
    ).order_by('date')
    
    return render(request, 'msys42app/view_annual_medical_check.html', {
        'child': child,
        'year': year,
        'medical_checks': medical_checks,
        'today': date.today().isoformat(),
    })

@login_required
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
        'medical_check': medical_check,
        'today': date.today().isoformat(),
    })

@login_required
def delete_annual_medical_check(request, child_id, check_id):
    child = get_object_or_404(Child, id=child_id)
    medical_check = get_object_or_404(AnnualMedicalCheck, id=check_id, child=child)
    
    try:
        medical_check.delete()
    except Exception as e:
        print(f"Error deleting medical check: {str(e)}")
        messages.error(request, f"Error deleting medical check: {str(e)}")
        
    return redirect('annual_medical_check_list', child_id=child_id)

@login_required
def edit_physicians_exam(request, pk, id):
    child = get_object_or_404(Child, pk=pk)
    exam = get_object_or_404(PhysiciansExam, pk=id)
    exams = PhysiciansExam.objects.filter(child=child).exclude(pk=id)
    
    # Get all years from 1900 to current year
    current_year = datetime.now().year
    all_years = list(range(current_year, 1899, -1))
    # Get years already used by other exams for this child
    used_years = exams.values_list('year', flat=True)
    # Available years are those not already used plus the current exam's year
    available_years = [y for y in all_years if y not in used_years or y == exam.year]

    if request.method == "POST":
        year = request.POST.get('year')
        
        # Validate that the year is not already used by another exam
        year_exists = PhysiciansExam.objects.filter(child=child, year=year).exclude(pk=id).exists()
        if year_exists:
            messages.error(request, f"A physician's exam for year {year} already exists for this child.")
            return render(request, 'msys42app/edit_phyexam.html', {
                'child': child, 
                'exam': exam, 
                'available_years': available_years,
                'error': f"A physician's exam for year {year} already exists for this child."
            })
        
        # Validate that the year is not in the future
        if int(year) > current_year:
            messages.error(request, "Year cannot be in the future.")
            return render(request, 'msys42app/edit_phyexam.html', {
                'child': child, 
                'exam': exam, 
                'available_years': available_years,
                'error': "Year cannot be in the future."
            })
            
        # grade = request.POST.get('grade')
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
        other_label = request.POST.get('other_label', '')
        other = request.POST.get('other', 'NE')
        clear_other = request.POST.get('clear_other', 'false')

        exam.year = year
        # exam.grade = grade
        exam.height = height
        exam.weight = weight
        exam.bp = bp
        exam.vision_right = vision_right
        exam.vision_left = vision_left
        exam.hearing_right = hearing_right
        exam.hearing_left = hearing_left
        exam.eyes = eyes
        exam.ears = ears
        exam.nose = nose
        exam.throat = throat
        exam.teeth = teeth
        exam.heart = heart
        exam.lungs = lungs
        exam.abdomen = abdomen
        exam.nervous_system = nervous_system
        exam.skin = skin
        exam.nutrition = nutrition

        # Set other fields to None by default if explicitly cleared
        if clear_other == 'true':
            exam.other_label = None
            exam.other = None
        # Only update other fields if they are provided and not empty
        elif other_label and other_label.strip():
            exam.other_label = other_label
            exam.other = other

        exam.save()
        return redirect('view_physicians_exam', pk=child.pk, id=exam.pk)

    return render(request, 'msys42app/edit_phyexam.html', {'child': child, 'exam': exam, 'available_years': available_years})

@login_required
def delete_physicians_exam(request, pk, id):
    child = get_object_or_404(Child, pk=pk)
    exam = get_object_or_404(PhysiciansExam, pk=id)
    
    if request.method == 'POST':
        exam.delete()
        return redirect('home_physicians_exam', pk=child.pk)
    
    return render(request, 'msys42app/delete_phyexam.html', {'child': child, 'exam': exam})
