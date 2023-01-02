from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import NewUser, PhoneVal

class NewUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = NewUser
        fields = ('username', 'phone_number', 'password1', 'password2')
        
class NewUserChangeForm(UserChangeForm):
    class Meta:
        model = NewUser
        fields = ('email', 'first_name', 'last_name', 'date_of_birth', 'phone_number')
        
class NewUserForm(forms.ModelForm):
    class Meta:
        model = NewUser
        fields = ('email', 'first_name', 'last_name', 'date_of_birth', 'occupation')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 'id': 'email', 'placeholder': 'example@email.com'
                }), 
            'first_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'first_name', 'placeholder': 'Your name'
                }), 
            'last_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'last_name', 'placeholder': 'Your last name'
                }), 
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control', 'id': 'date_of_birth', 'placeholder': '2000/12/30', 'type': 'date'
                }), 
            'occupation': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'occupation', 'placeholder': 'Your occupation'
                })
        }

class PhoneValForm(forms.ModelForm):
    class Meta:
        model = PhoneVal
        fields = '__all__'