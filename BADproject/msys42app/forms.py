from django import forms
import datetime
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

# Education

def get_school_year_choices(start=2010):
    current_year = datetime.datetime.now().year
    end_year = current_year + 1  # ensure next academic year is included
    choices = []
    for y in range(start, end_year):
        label = f"{y}–{y+1}"
        choices.append((label, label))
    return choices

class EducationForm(forms.ModelForm):
    year = forms.ChoiceField(
        choices=get_school_year_choices(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Education
        fields = ['year', 'grade']
        widgets = {
            'grade': forms.Select(attrs={'class': 'form-control'}),
        }

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
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'height: 50px; width: 100%; font-size: 1rem; padding: 10px;'
        })
    )
    medical_status_history = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'style': 'min-height: 120px; width: 100%; font-size: 1rem; padding: 10px; resize: vertical;'
        })
    )
    disability_status = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'height: 50px; width: 100%; font-size: 1rem; padding: 10px;'
        })
    )
    disability_status_history = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'style': 'min-height: 120px; width: 100%; font-size: 1rem; padding: 10px; resize: vertical;'
        })
    )
    allergies_history = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'style': 'min-height: 120px; width: 100%; font-size: 1rem; padding: 10px; resize: vertical;'
        })
    )
    allergies_conditions = forms.MultipleChoiceField(
        choices=ALLERGY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    other_condition = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'height: 50px; width: 100%; font-size: 1rem; padding: 10px; margin-top: 10px;',
            'placeholder': 'Please specify other condition'
        })
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
year_choices = [(year, year) for year in range(2000, datetime.datetime.now().year + 1)]
conditions = [("N", "N"), ("A", "A"), ("C", "C"), ("R", "R")]

class PhysiciansExamForm(forms.ModelForm):
    child = forms.ModelChoiceField(queryset=Child.objects.all(), required=True)
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
