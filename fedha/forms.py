
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

from .models import Claim

from django.forms.widgets import PasswordInput, TextInput 

from .models import Policy


#Create/Register a user(Model Form)
class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']


# - Authenticate a user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


#form for adding new policies
class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['policy_number', 'policy_holder_name', 'policy_type', 'start_date', 'end_date', 'premium_amount', 'coverage_amount', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

#Policy application form
class PolicyApplicationForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = [
             'policy_holder_name', 'policy_type', 'policy_holder_name', 'start_date', 
            'end_date', 'premium_amount', 'coverage_amount', 'status'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'premium_amount': forms.NumberInput(attrs={'min': 0}),
            'coverage_amount': forms.NumberInput(attrs={'min': 0}),
        }   

#Claim submission form
class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['claim_amount', 'claim_reason']
        widgets = {
            'claim_reason': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    claim_amount = forms.DecimalField(max_digits=10, decimal_places=2)
    claim_reason = forms.CharField(widget=forms.Textarea, max_length=1000)

class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['policy_type']  # Replace with the fields you have in your Policy model



