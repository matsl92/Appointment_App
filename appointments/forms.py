from django import forms
from .models import Week, Gap
from datetime import date, timedelta

def get_next_start_date():
    try:
        x = Gap.objects.last().date_and_time.date() + timedelta(days=1)
        print(x)
    except:
        x = date.today()
    return x

next_start_date = get_next_start_date()
        
class WeekForm(forms.ModelForm):
    class Meta:
        model = Week
        fields = '__all__'
        widgets = {
            'minutes_per_appointment': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'minutes_per_appointment', 'placeholder': '30', 'min': '30'
                }), 
            'start_date': forms.DateInput(attrs={
                'class': 'form-control', 'id': 'start_date', 'placeholder': 'Start date', 'type': 'date',
                'min': date.today().strftime("%Y-%m-%d"),
                'value': next_start_date.strftime("%Y-%m-%d")
                }), 
            'monday_start': forms.TimeInput(attrs={
                'class': 'form-control', 'id': 'monday_start', 'placeholder': 'start hour for monday', 'type': 'time'
                }), 
            'monday_end': forms.TimeInput(attrs={
                'class': 'form-control', 'id': 'monday_end', 'placeholder': 'End hour for monday', 'type': 'time'
                }), 
            'tuesday_start': forms.TimeInput(attrs={
                'class': 'form-control', 'id': 'tuesday_start', 'placeholder': 'start hour for tuesday', 'type': 'time'
                }), 
            'tuesday_end': forms.TimeInput(attrs={
                'class': 'form-control', 'id': 'tuesday_end', 'placeholder': 'End hour for tuesday', 'type': 'time'
                }),
            'wednesday_start': forms.TimeInput(attrs={
                'class': 'form-control', 'id': 'wednesday_start', 'placeholder': 'start hour for wednesday', 'type': 'time'
                }), 
            'wednesday_end': forms.TimeInput(attrs={
                'class': 'form-control', 'id': 'wednesday_end', 'placeholder': 'End hour for wednesday', 'type': 'time'
                }),
            'thursday_start': forms.TimeInput(attrs={
                'class': 'form-control', 'id': 'thursday_start', 'placeholder': 'start hour for thursday', 'type': 'time'
                }), 
            'thursday_end': forms.TimeInput(attrs={
                'class': 'form-control', 'id': 'thursday_end', 'placeholder': 'End hour for thursday', 'type': 'time'
                }),
            'friday_start': forms.TimeInput(attrs={
                'class': 'form-control', 'id': 'friday_start', 'placeholder': 'start hour for friday', 'type': 'time'
                }), 
            'friday_end': forms.TimeInput(attrs={
                'class': 'form-control', 'id': 'friday_end', 'placeholder': 'End hour for friday', 'type': 'time'
                }),
            'saturday_start': forms.TimeInput(attrs={
                'class': 'form-control', 'id': 'saturday_start', 'placeholder': 'start hour for saturday', 'type': 'time'
                }), 
            'saturday_end': forms.TimeInput(attrs={
                'class': 'form-control', 'id': 'saturday_end', 'placeholder': 'End hour for saturday', 'type': 'time'
                }),
            'sunday_start': forms.TimeInput(attrs={
                'class': 'form-control', 'id': 'sunday_start', 'placeholder': 'start hour for sunday', 'type': 'time'
                }), 
            'sunday_end': forms.TimeInput(attrs={
                'class': 'form-control', 'id': 'sunday_end', 'placeholder': 'End hour for sunday', 'type': 'time'
                }),
        }