from django.contrib.auth.models import User
from Clinic.models import Visits, Results, Doctors, Patient, Messages, Facility
from django import forms
from django.forms import ValidationError, widgets
from mapwidgets.widgets import GoogleStaticMapWidget, GoogleStaticOverlayMapWidget, GooglePointFieldWidget
from django import forms
from Clinic.models import Facility
from mapwidgets.widgets import GoogleStaticMapWidget
from bootstrap_datepicker_plus import DatePickerInput


class FacilityDetailForm(forms.ModelForm):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Facility
        fields = ("name", "coordinates")
        widgets = {
            'coordinates': GoogleStaticMapWidget(),
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_conf = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'password_conf']


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput)
    last_name = forms.CharField(widget=forms.TextInput)
    email = forms.CharField(widget=forms.TextInput)
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Messages
        fields = ['first_name', 'last_name', 'email', 'text']


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


class YourAccountForm(forms.Form):
    image = forms.ImageField()



