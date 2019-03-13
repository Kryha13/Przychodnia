from django.contrib.auth.models import User
from Clinic.models import Visits, Results, Doctors, Patient
from django import forms
from django.forms import ValidationError, widgets


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_conf = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'password_conf']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class VisitsHistoryForm(forms.ModelForm):
    class Meta:
        model = Visits
        fields = ['doctor', 'date']


class TreatmentHistoryForm(forms.ModelForm):
    class Meta:
        model = Results
        fields = ['patient', 'visit', 'paper']


hours = {
        ('8:00', '8:00'),
        ('9:00', '9:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00')
         }


class SetVisitForm(forms.ModelForm):

    date = forms.CharField(widget=forms.SelectDateWidget)
    hour = forms.ChoiceField(choices=hours)

    class Meta:
        model = Visits
        fields = ['patient', 'doctor', 'date', 'hour']


class YourAccountForm(forms.Form):
    image = forms.ImageField()


