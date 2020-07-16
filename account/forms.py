from django import forms
from .models import Account
from  bookings.models import MedicalAid
from django.forms import ModelForm
from bookings.models import Dependencies, Patient



class RegisterForm(forms.Form):
    first_name = forms.CharField(label='You name', max_length=50)
    last_name = forms.CharField(label='You last  name', max_length=50)
    email = forms.EmailField(label='Email')
    phone_number = forms.CharField(label='Phone', max_length=50)
    date_of_birth = forms.DateField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='ConFirm Password', widget=forms.PasswordInput)
    GENDER = (
        ("M", "MALE"),
        ("F", "FEMALE")
    )
    gender = forms.ChoiceField(choices=GENDER)
    medical_aid= forms.ModelChoiceField(queryset= MedicalAid.objects.all(), required=False)
    medical_aid_number = forms.CharField(label='Medical Aid Number', max_length=20, required=False)


    def clean(self):
        cleaned_data= super().clean()
        password1_data= self.cleaned_data.get('password1')
        password2_data= self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')

        user = Account.objects.user_exist(email.lower())

        madical_aid_number = self.cleaned_data.get('medical_aid_number')
        medical_aid = self.cleaned_data.get('medical_aid')
        if medical_aid is not None and madical_aid_number=='':
            raise forms.ValidationError("Please insert the number of your medical aid")
        if user.count()>0:
            raise forms.ValidationError("This Email is already registered")
        if password1_data != password2_data:
            raise forms.ValidationError("Passwords did not match")


class DependenciesForm(ModelForm):
    class Meta:
        model = Dependencies
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'patient']
        widgets = {
            'patient': forms.HiddenInput(),
        }


class LoginForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', 
                            widget=forms.PasswordInput())
        
