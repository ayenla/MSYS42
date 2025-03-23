from django import forms
from .models import MedicalHistory, Immunization, AllergyCondition


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