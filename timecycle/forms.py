from django import forms
from .models import MetaCycle, Activity

class MetaCycleForm(forms.ModelForm):
    class Meta:
        model = MetaCycle
        fields = ['name', 'start_date', 'end_date', 'frequency']  # Include frequency field for selecting days
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'frequency': forms.CheckboxSelectMultiple(),
        }

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['meta_cycle', 'name' , 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type':'time'}),
            'end_time': forms.TimeInput(attrs={'type':'time'})
        }
