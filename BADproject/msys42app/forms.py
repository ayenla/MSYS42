from django import forms
import datetime
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.core.validators import MaxLengthValidator

# Education
#

def get_school_year_choices(start=2000, used_years=None):
    current_year = datetime.datetime.now().year
    end_year = current_year + 1

    # Defer DB access to caller; default to empty during import
    used_years = set(used_years or [])

    choices = []
    for y in range(start, end_year):
        label = f"{y}–{y+1}"
        if label not in used_years:
            choices.append((label, label))  # value and label are the same

    choices.reverse()  # most recent first
    return choices

class EducationForm(forms.ModelForm):
    year = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Education
        fields = ['year', 'grade']
        widgets = {
            'grade': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Safely populate year choices at runtime to avoid import-time DB hits
        used_years = []
        try:
            used_years = Education.objects.values_list('year', flat=True)
        except Exception:
            # During migrations or before tables exist, silently fall back
            used_years = []
        self.fields['year'].choices = get_school_year_choices(used_years=used_years)

# Medical History
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

class MedicalHistoryForm(forms.ModelForm):
    medical_status = forms.CharField(
        required=False,
        max_length=255,
        validators=[MaxLengthValidator(255)],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'height: 50px; width: 100%; font-size: 1rem; padding: 10px;',
            'maxlength': '255'
        }),
        error_messages={
            'max_length': 'Inputted text exceeds the maximum possible character count of 255.'
        }
    )
    medical_status_history = forms.CharField(
        required=False,
        max_length=255,
        validators=[MaxLengthValidator(255)],
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'style': 'min-height: 120px; width: 100%; font-size: 1rem; padding: 10px; resize: vertical;',
            'maxlength': '255'
        }),
        error_messages={
            'max_length': 'Inputted text exceeds the maximum possible character count of 255.'
        }
    )
    disability_status = forms.CharField(
        required=False,
        max_length=255,
        validators=[MaxLengthValidator(255)],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'height: 50px; width: 100%; font-size: 1rem; padding: 10px;',
            'maxlength': '255'
        }),
        error_messages={
            'max_length': 'Inputted text exceeds the maximum possible character count of 255.'
        }
    )
    disability_status_history = forms.CharField(
        required=False,
        max_length=255,
        validators=[MaxLengthValidator(255)],
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'style': 'min-height: 120px; width: 100%; font-size: 1rem; padding: 10px; resize: vertical;',
            'maxlength': '255'
        }),
        error_messages={
            'max_length': 'Inputted text exceeds the maximum possible character count of 255.'
        }
    )
    allergies_history = forms.CharField(
        required=False,
        max_length=255,
        validators=[MaxLengthValidator(255)],
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'style': 'min-height: 120px; width: 100%; font-size: 1rem; padding: 10px; resize: vertical;',
            'maxlength': '255'
        }),
        error_messages={
            'max_length': 'Inputted text exceeds the maximum possible character count of 255.'
        }
    )
    allergies_conditions = forms.MultipleChoiceField(
        choices=ALLERGY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    other_condition = forms.CharField(
        required=False,
        max_length=255,
        validators=[MaxLengthValidator(255)],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'height: 50px; width: 100%; font-size: 1rem; padding: 10px; margin-top: 10px;',
            'placeholder': 'Please specify other condition',
            'maxlength': '255'
        }),
        error_messages={
            'max_length': 'Inputted text exceeds the maximum possible character count of 255.'
        }
    )

    class Meta:
        model = MedicalHistory
        fields = [
            'medical_status',
            'medical_status_history',
            'disability_status',
            'disability_status_history',
            'allergies_conditions',
            'allergies_history',
            'other_condition'
        ]
        
    def clean(self):
        cleaned_data = super().clean()
        
        # Check each field for max length
        fields_to_check = [
            'medical_status', 
            'medical_status_history', 
            'disability_status', 
            'disability_status_history', 
            'allergies_history', 
            'other_condition'
        ]
        
        for field_name in fields_to_check:
            value = cleaned_data.get(field_name, '')
            if value:
                # Trim the value to handle any whitespace issues
                trimmed_value = value.strip()
                value_length = len(trimmed_value)
                print(f"Field {field_name} length: {value_length}")
                
                # Only raise error if strictly greater than 255
                if value_length > 255:
                    self.add_error(
                        field_name, 
                        f'Inputted text exceeds the maximum possible character count of 255. Current length: {value_length}'
                    )
        
        return cleaned_data

class ImmunizationForm(forms.ModelForm):
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control w-100',
            'style': 'height: 50px; font-size: 1rem; padding: 10px;'
        })
    )
    immunization_given = forms.CharField(required=False)

    class Meta:
        model = Immunization
        fields = ['date', 'immunization_given']
        widgets = {
            'immunization_given': forms.TextInput(attrs={
                'class': 'form-control w-100',
                'style': 'height: 50px; font-size: 1rem; padding: 10px;'
            })
        }
        
    def clean(self):
        cleaned_data = super().clean()
        
        # If the form is marked for deletion, skip validation
        if cleaned_data.get('DELETE', False):
            return cleaned_data
            
        date = cleaned_data.get('date')
        immunization = cleaned_data.get('immunization_given')
        
        # If one field is filled, the other must be too
        if (date and not immunization) or (not date and immunization):
            raise forms.ValidationError("Both date and immunization must be provided together.")
            
        # If both fields are empty and it's not marked for deletion, the form is effectively empty
        # Just return it as is for formset management to handle it
        if not date and not immunization and not self.cleaned_data.get('DELETE', False):
            pass
            
        return cleaned_data

year_choices = [(year, year) for year in range(2000, datetime.datetime.now().year + 1)]
conditions = [("N", "N"), ("A", "A"), ("C", "C"), ("R", "R")]

class PhysiciansExamForm(forms.ModelForm):
    child = forms.ModelChoiceField(queryset=Child.objects.none(), required=True)
    year = forms.ChoiceField(choices=year_choices, required=True)
    grade = forms.ChoiceField(choices=conditions, required=True)
    height = forms.ChoiceField(choices=conditions, required=True)
    weight = forms.ChoiceField(choices=conditions, required=True)
    bp = forms.ChoiceField(choices=conditions, required=True)
    vision_right = forms.ChoiceField(choices=conditions, required=True)
    vision_left = forms.ChoiceField(choices=conditions, required=True)
    hearing_right = forms.ChoiceField(choices=conditions, required=True)
    hearing_left = forms.ChoiceField(choices=conditions, required=True)
    eyes = forms.ChoiceField(choices=conditions, required=True)
    ears = forms.ChoiceField(choices=conditions, required=True)
    nose = forms.ChoiceField(choices=conditions, required=True)
    throat = forms.ChoiceField(choices=conditions, required=True)
    teeth = forms.ChoiceField(choices=conditions, required=True)
    heart = forms.ChoiceField(choices=conditions, required=True)
    lungs = forms.ChoiceField(choices=conditions, required=True)
    abdomen = forms.ChoiceField(choices=conditions, required=True)
    nervous_system = forms.ChoiceField(choices=conditions, required=True)
    skin = forms.ChoiceField(choices=conditions, required=True)
    nutrition = forms.ChoiceField(choices=conditions, required=True)
    other = forms.ChoiceField(choices=conditions, required=False)
    other_label = forms.CharField(max_length=20, required=False)

    class Meta:
        model = PhysiciansExam
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['child'].queryset = Child.objects.all()
        except Exception:
            self.fields['child'].queryset = Child.objects.none()

class AnnualMedicalCheckForm(forms.ModelForm):
    height = forms.DecimalField(
        max_digits=5,
        decimal_places=1,
        min_value=0,
        max_value=999.9,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control w-100',
            'style': 'height: 50px; font-size: 1rem; padding: 10px;',
            'step': '0.1'
        })
    )
    weight = forms.DecimalField(
        max_digits=5,
        decimal_places=1,
        min_value=0,
        max_value=999.9,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control w-100',
            'style': 'height: 50px; font-size: 1rem; padding: 10px;',
            'step': '0.1'
        })
    )
    hemoglobin = forms.DecimalField(
        max_digits=4,
        decimal_places=1,
        min_value=0,
        max_value=99.9,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control w-100',
            'style': 'height: 50px; font-size: 1rem; padding: 10px;',
            'step': '0.1'
        })
    )
    condition = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control w-100',
            'rows': 4,
            'style': 'min-height: 100px; font-size: 1rem; padding: 10px; resize: vertical;'
        })
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control w-100',
            'rows': 4,
            'style': 'min-height: 100px; font-size: 1rem; padding: 10px; resize: vertical;'
        })
    )

    class Meta:
        model = AnnualMedicalCheck
        fields = ['date', 'height', 'weight', 'hemoglobin', 'condition', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control w-100',
                'style': 'height: 50px; font-size: 1rem; padding: 10px;',
                'required': 'required'
            })
        }

    def __init__(self, *args, **kwargs):
        self.child = kwargs.pop('child', None)
        super().__init__(*args, **kwargs)

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            raise forms.ValidationError("Please select a date.")
        
        # Check if there's already a medical check for this year
        if self.child and date:
            year = date.year
            existing_check = AnnualMedicalCheck.objects.filter(
                child=self.child,
                date__year=year
            ).exists()
            
            if existing_check:
                raise forms.ValidationError(f"A medical check already exists for the year {year}.")
        
        return date

class LoginForm(AuthenticationForm):
    """Form for user login"""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class UserRegistrationForm(UserCreationForm):
    """Form for user registration, used by admins to create new user accounts"""
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
        # Remove email field completely
        if 'email' in self.fields:
            del self.fields['email']

class UserEditForm(UserChangeForm):
    """Form for editing user information"""
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')
