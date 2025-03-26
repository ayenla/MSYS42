from django import forms
import datetime
from .models import *


ALLERGY_CHOICES = [
    ("asthma", "Asthma"),
    ("behavioral_problem", "Behavioral Problem"),
    ("heart_disease", "Heart Disease"),
    ("hypertension", "Hypertension"),
    ("malaria", "Malaria"),
    ("cancer", "Cancer"),
    ("chronic_cough", "Chronic Cough/Wheezing"),
    ("arthritis", "IRA Arthritic"),
    ("seizures", "Seizures"),
    ("jaundice", "Jaundice"),
    ("diabetes", "Diabetes"),
    ("hearing_problem", "Hearing Problem"),
    ("sickle_cell_anemia", "Sickle Cell Anemia"),
    ("skin_problem", "Skin Problem"),
    ("vision_problem", "Vision Problem"),
]

class MedicalHistoryForm(forms.ModelForm):
    medical_status = forms.CharField(required=False)
    medical_status_history = forms.CharField(required=False)
    disability_status = forms.CharField(required=False)
    disability_status_history = forms.CharField(required=False)
    allergies_history = forms.CharField(required=False)
    allergies_conditions = forms.MultipleChoiceField(
        choices=ALLERGY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = MedicalHistory
        fields = [
            'medical_status',
            'medical_status_history',
            'disability_status',
            'disability_status_history',
            'allergies_conditions',
            'allergies_history'
        ]
        widgets = {
            'medical_status': forms.TextInput(attrs={
                'class': 'form-control w-100',
                'style': 'height: 50px; font-size: 1rem; padding: 10px;'
            }),
            'medical_status_history': forms.Textarea(attrs={
                'class': 'form-control w-100',
                'rows': 8,
                'style': 'min-height: 200px; font-size: 1rem; padding: 10px; resize: vertical;'
            }),
            'disability_status': forms.TextInput(attrs={
                'class': 'form-control w-100',
                'style': 'height: 50px; font-size: 1rem; padding: 10px;'
            }),
            'disability_status_history': forms.Textarea(attrs={
                'class': 'form-control w-100',
                'rows': 8,
                'style': 'min-height: 200px; font-size: 1rem; padding: 10px; resize: vertical;'
            }),
            'allergies_history': forms.Textarea(attrs={
                'class': 'form-control w-100',
                'rows': 8,
                'style': 'min-height: 200px; font-size: 1rem; padding: 10px; resize: vertical;'
            }),
        }

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
    other = forms.ChoiceField(choices=conditions, required=True)
    other_label = forms.CharField(max_length=20)

    class Meta:
        model = PhysiciansExam
        fields = "__all__"

class AnnualMedicalCheckForm(forms.ModelForm):
    class Meta:
        model = AnnualMedicalCheck
        fields = ['date', 'height', 'weight', 'hemoglobin', 'condition', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control w-100',
                'style': 'height: 50px; font-size: 1rem; padding: 10px;'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control w-100',
                'style': 'height: 50px; font-size: 1rem; padding: 10px;',
                'step': '0.01'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control w-100',
                'style': 'height: 50px; font-size: 1rem; padding: 10px;',
                'step': '0.01'
            }),
            'hemoglobin': forms.NumberInput(attrs={
                'class': 'form-control w-100',
                'style': 'height: 50px; font-size: 1rem; padding: 10px;',
                'step': '0.01'
            }),
            'condition': forms.Textarea(attrs={
                'class': 'form-control w-100',
                'rows': 4,
                'style': 'min-height: 100px; font-size: 1rem; padding: 10px; resize: vertical;'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control w-100',
                'rows': 4,
                'style': 'min-height: 100px; font-size: 1rem; padding: 10px; resize: vertical;'
            }),
        }
